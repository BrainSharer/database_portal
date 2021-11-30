from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, views
from rest_framework import permissions
from django.http import JsonResponse, HttpResponse
from django.templatetags.static import static
from rest_framework.response import Response
from django.utils.html import escape
from django.http import Http404
from django.db.models import Q
import string
import random
from collections import defaultdict
import numpy as np
import os
import pandas as pd
from scipy.interpolate import splprep, splev
from neuroglancer.serializers import AnnotationSerializer, \
    AnnotationsSerializer, LineSerializer, NeuroglancerSerializer, \
    IdSerializer, NeuronSerializer, AnatomicalRegionSerializer
from neuroglancer.models import InputType, NeuroglancerModel, LayerData, Structure
from neuroglancer.atlas import get_scales, make_ontology_graph_CCFv3, make_ontology_graph_pma
from neuroglancer.models import InputType, NeuroglancerModel, LayerData, Structure, \
    MouselightNeuron

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class NeuroglancerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the neuroglancer states to be viewed or edited.
    """
    queryset = NeuroglancerModel.objects.all()
    serializer_class = NeuroglancerSerializer
    permission_classes = [permissions.AllowAny]

class NeuroglancerDataView(views.APIView):
    """This will be run when a a ID is sent to:
    https://site.com/activebrainatlas/urldata?id=999
    Where 999 is the primary key of the url model"""

    def get(self, request, *args, **kwargs):
        # Validate the incoming input (provided through query parameters)
        serializer = IdSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data['id']
        neuroglancerModel = NeuroglancerModel.objects.get(pk=id)
        return HttpResponse(f"#!{escape(neuroglancerModel.neuroglancer_state)}")

class Annotation(views.APIView):
    """
    Fetch LayerData model and return parsed annotation layer.
    neuroglancer is of the the form
    https://activebrainatlas.ucsd.edu/activebrainatlas/annotation/DKXX/premotor/2
    Where:
         DKXX is the animal,
         premotor is the layer name,
         2 is the input type ID
    """
    def get(self, request, prep_id, layer_name, input_type_id, format=None):
        data = []
        try:
            rows = LayerData.objects.filter(prep_id=prep_id)\
                        .filter(layer=layer_name)\
                        .filter(input_type_id=input_type_id)\
                        .filter(active=True)\
                        .order_by('section', 'id').all()
        except LayerData.DoesNotExist:
            raise Http404
        scale_xy, z_scale = get_scales(prep_id)
        for row in rows:
            point_dict = {}
            point_dict['type'] = 'point'
            point_dict['id'] = random_string()
            point_dict['point'] = \
                [int(round(row.x/scale_xy)), int(round(row.y/scale_xy)), int(round(row.section/z_scale))]
            point_dict['description'] = ""
            data.append(point_dict)
        serializer = AnnotationSerializer(data, many=True)
        return Response(serializer.data)

class Annotations(views.APIView):
    """
    Fetch NeuroglancerModel and return a set of two dictionaries. 
    One is from the layer_data
    table and the other is the COMs that have been set as transformations.
    {'id': 213, 'description': 'DK39 COM Test', 'layer_name': 'COM'}
    url is of the the form:
    https://activebrainatlas.ucsd.edu/activebrainatlas/annotations
    """

    def get(self, request, format=None):
        """
        This will get the layer_data
        """
        data = []
        layers = LayerData.objects.order_by('prep_id', 'layer', 'input_type_id')\
            .filter(active=True)\
            .filter(layer__isnull=False)\
            .values('prep_id', 'layer','input_type__input_type','input_type_id')\
            .distinct()
        for layer in layers:
            data.append({
                "prep_id":layer['prep_id'],
                "layer":layer['layer'],
                "input_type":layer['input_type__input_type'],
                "input_type_id":layer['input_type_id'],                
                })

        serializer = AnnotationsSerializer(data, many=True)
        return Response(serializer.data)

class MouseLightNeuron(views.APIView):
    """
    Fetch MouseLight neurons meeting filter criteria 
    url is of the the form
    mlneurons/<str:atlas_name>/<str:brain_region1>/<str:filter_type1>/<str:operator_type1>/<int:thresh1>/<str:filter_type2>/<str:operator_type2>/<int:thresh2>
    Where:
        atlas_name     <str> : required, either "ccfv3_25um" or "pma_20um"
        brain_region1  <str> : required, e.g. "Cerebellum"
        filter_type1   <str> : optional, e.g. "soma", "axon_endpoints", ...
        operator_type1 <str> : optional, e.g. "gte" -> "greater than or equal to"
        thresh1        <int> : optional, e.g. 2 
        brain_region2  <str> : optional, e.g. "Thalamus"
        filter_type2   <str> : optional, e.g. "dendritic_branchpoints"
        operator_type2 <str> : optional, e.g. "eq" -> "exactly equal to"
        thresh2        <int> : optional, e.g. 5
    """

    def get(self, request, atlas_name, brain_region1, 
        filter_type1='soma', operator_type1=None, thresh1=None,
        brain_region2=None, filter_type2=None, operator_type2=None, thresh2=None):
        
        print(atlas_name,brain_region1,filter_type1,
            operator_type1,thresh1,brain_region2,
            filter_type2,operator_type2,thresh2)
        
        if atlas_name == 'ccfv3_25um':
            ontology_graph = make_ontology_graph_CCFv3()
        elif atlas_name == 'pma_25um':
            ontology_graph = make_ontology_graph_pma()
        
        # filter to only get neurons in this atlas
        rows = MouselightNeuron.objects.filter(annotation_space__exact=atlas_name)
        
        # Filter #1, required
        brain_region_id1 = ontology_graph.get_id(brain_region1)
        if filter_type1 == 'soma':
            # Figure out all progeny of this region since neuron could be in this shell or any child
            progeny = ontology_graph.get_progeny(brain_region1)
            progeny_ids = [ontology_graph.get_id(prog) for prog in progeny]
            ids_tosearch = [brain_region_id1] + progeny_ids
            print(ids_tosearch)
            rows = rows.filter(soma_atlas_id__in=ids_tosearch)
        else:
            filter_name1 = f'{filter_type1}_dict__count_{brain_region_id1}__{operator_type1}'
            filter1 = Q(**{filter_name1:thresh1})
            if operator_type1 in ['gte','lte','exact'] and thresh1 == 0:
                filter_name1_nullcheck = f'{filter_type1}_dict__count_{brain_region_id1}__isnull'
                filter1_nullcheck = Q(**{filter_name1_nullcheck:True})
                rows = rows.filter(filter1 | filter1_nullcheck)
            else:
                rows = rows.filter(filter1)
        # Filter #2, optional
        if filter_type2:
            brain_region_id2 = ontology_graph.get_id(brain_region2)
            print(brain_region_id2)
            if filter_type2 == 'soma':
                # Figure out all progeny of this region since neuron could be in this shell or any child
                progeny = ontology_graph.get_progeny(brain_region1)
                progeny_ids = [ontology_graph.get_id(prog) for prog in progeny]
                ids_tosearch = [brain_region_id2] + progeny_ids
                rows = rows.filter(soma_atlas_id__in=ids_tosearch)
            else:
                filter_name2 = f'{filter_type2}_dict__count_{brain_region_id2}__{operator_type2}'
                filter2 = Q(**{filter_name2:thresh2})
                if operator_type2 in ['gte','lte','exact'] and thresh2 == 0:
                    filter_name2_nullcheck = f'{filter_type2}_dict__count_{brain_region_id2}__isnull'
                    filter2_nullcheck = Q(**{filter_name2_nullcheck:True})
                    rows = rows.filter(filter2 | filter2_nullcheck)
                else:
                    rows = rows.filter(filter2)
        print(rows)
        neuron_indices = [x-1 for x in rows.values_list('id',flat=True)]
        skeleton_segment_ids = [ix*3+x for ix in neuron_indices for x in [0,1,2]]
        serializer = NeuronSerializer({'segmentId':skeleton_segment_ids})
        return Response(serializer.data)

class AnatomicalRegions(views.APIView):
    """
    Fetch the complete list of anatomical brain regions
    url is of the the form
    /anatomicalregions/atlasName
    """

    def get(self, request, atlas_name):
        if atlas_name == 'ccfv3_25um':
            ontology_graph = make_ontology_graph_CCFv3()
        elif atlas_name == 'pma_25um':
            ontology_graph = make_ontology_graph_pma()
        segment_names = list(ontology_graph.graph.keys())
        serializer = AnatomicalRegionSerializer({'segment_names':segment_names})
        return Response(serializer.data)

def interpolate(points, new_len):
    points = np.array(points)
    pu = points.astype(int)
    indexes = np.unique(pu, axis=0, return_index=True)[1]
    points = np.array([points[index] for index in sorted(indexes)])
    addme = points[0].reshape(1, 2)
    points = np.concatenate((points, addme), axis=0)

    tck, u = splprep(points.T, u=None, s=3, per=1)
    u_new = np.linspace(u.min(), u.max(), new_len)
    x_array, y_array = splev(u_new, tck, der=0)
    arr_2d = np.concatenate([x_array[:, None], y_array[:, None]], axis=1)
    return list(map(tuple, arr_2d))

def get_input_type_id(input_type):
    input_type_id = 0
    try:
        input_types = InputType.objects.filter(input_type=input_type).filter(active=True).all()
    except InputType.DoesNotExist:
        raise Http404

    if len(input_types) > 0:
        input_type = input_types[0]
        input_type_id = input_type.id

    return input_type_id

def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
        
def load_layers(request):
    layers = []
    url_id = request.GET.get('id')
    neuroglancerModel = NeuroglancerModel.objects.get(pk=url_id).all()
    if neuroglancerModel.layers is not None:
        layers = neuroglancerModel.layers
    return render(request, 'layer_dropdown_list_options.html', {'layers': layers})

def public_list(request):
    """
    Shows a listing of urls made available to the public
    :param request:
    :return:
    """
    neuroglancer_states = NeuroglancerModel.objects.filter(public=True).order_by('comments')
    return render(request, 'public.html', {'neuroglancer_states': neuroglancer_states})

class LandmarkList(views.APIView):

    def get(self, request, format=None):

        list_of_landmarks = Structure.objects.all().filter(active = True).all()
        list_of_landmarks = [i.abbreviation for i in list_of_landmarks]
        data = {}
        data['land_marks'] = list_of_landmarks
        return JsonResponse(data)