from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, views
from rest_framework import permissions
from django.http import JsonResponse, HttpResponse
from django.templatetags.static import static
from rest_framework.response import Response
from django.utils.html import escape
from django.http import Http404
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
from neuroglancer.atlas import get_scales, make_ontology_graphCCFv3
from neuroglancer.models import InputType, NeuroglancerModel, LayerData, Structure

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
    /mlneuron/Cerebellum/2
    Where:
         Cerebellum: brain region,
         2: threshold, e.g. number of axonal endpoints >= 2
    """
    def __init__(self):
        self.mouselight_csv_file = os.path.join(settings.STATIC_ROOT,'neuroglancer/all_mouselight_neurons.csv')
        self.mouselight_df = pd.read_csv(self.mouselight_csv_file)

    def get(self, request, brain_region, filter_type,operator_type,thresh):
        ontology_graph = make_ontology_graphCCFv3()
        neurons = self.mouselight_df.loc[self.mouselight_df[f'{filter_type}_dict'].apply(
            self.filter_by_region,args=(ontology_graph,brain_region,thresh,operator_type))]
        skeleton_segment_ids = [ix*3+x for ix in neurons.index for x in [0,1,2]]
        serializer = NeuronSerializer({'segmentId':skeleton_segment_ids})
        return Response(serializer.data)

    def filter_by_region(self, dic, graph, region_name, thresh, operation):
        """ 
        Checks if dic[f'count_{region_name}'] (operation) thresh
        param: dic - dictionary where key in region ID and val is number of neurons with axonal endpoints in that region
        param: graph - ontology graph containing parent-child relationships between atlas regions 
        param: region_name - brain region name to check
        param: thresh - a neuron with # of axonal endpoints above this thresh will be returned
        param: operation - can be one of 'ge', 'le', or 'eq'
        """
        dic = eval(dic) # turns json string into dict type
        # First get region id
        region_id = graph.get_id(region_name) 

        # get all progeny (by name) 
        progeny_byname = graph.get_progeny(region_name)

        # convert to ids
        all_regions_byid = [region_id] + [graph.get_id(name) for name in progeny_byname]
        total_count = 0
        for ID in all_regions_byid:
            key = f'count_{ID}'
            if key not in dic:
                continue 
            total_count += dic[key]

        if operation == 'ge':
            return total_count >= thresh
        elif operation == 'le':
            return total_count <= thresh
        elif operation == 'eq':
            return total_count == thresh

class AnatomicalRegions(views.APIView):
    """
    Fetch the complete list of anatomical brain regions
    url is of the the form
    /anatomicalregions
    """

    def get(self, request):
        ontology_graph = make_ontology_graphCCFv3()
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