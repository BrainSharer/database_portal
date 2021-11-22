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
    AnnotationsSerializer, LineSerializer, UrlSerializer, IdSerializer, \
    NeuronSerializer
from neuroglancer.models import InputType, UrlModel, LayerData, Structure
from neuroglancer.atlas import get_scales, make_ontology_graphCCFv3

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class UrlViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the neuroglancer urls to be viewed or edited.
    """
    queryset = UrlModel.objects.all()
    serializer_class = UrlSerializer
    permission_classes = [permissions.AllowAny]

class UrlDataView(views.APIView):
    """This will be run when a a ID is sent to:
    https://site.com/activebrainatlas/urldata?id=999
    Where 999 is the primary key of the url model"""

    def get(self, request, *args, **kwargs):
        # Validate the incoming input (provided through query parameters)
        serializer = IdSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data['id']
        urlModel = UrlModel.objects.get(pk=id)
        return HttpResponse(f"#!{escape(urlModel.url)}")

class Annotation(views.APIView):
    """
    Fetch LayerData model and return parsed annotation layer.
    url is of the the form
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
        if input_type_id != 5:
            for row in rows:
                point_dict = {}
                point_dict['id'] = random_string()
                point_dict['point'] = \
                    [int(round(row.x/scale_xy)), int(round(row.y/scale_xy)), int(round(row.section/z_scale))]
                point_dict['type'] = 'point'
                if 'COM' or 'Rough Alignment' in layer_name:
                    point_dict['description'] = row.structure.abbreviation
                else:
                    point_dict['description'] = ""
                data.append(point_dict)
            serializer = AnnotationSerializer(data, many=True)
        else:
            data_dict = defaultdict(list)
            for row in rows:
                id = row.segment_id
                x = row.x / scale_xy
                y = row.y / scale_xy
                section = row.section / z_scale
                data_dict[(id, section)].append((x, y))
            for (k,section), points in data_dict.items():
                lp = len(points)
                if lp > 3:
                    new_len = max(lp, 200)
                    points = interpolate(points, new_len)
                    for i in range(new_len):
                        tmp_dict = {}
                        pointA = points[i]
                        try:
                            pointB = points[i+1]
                        except IndexError:
                            pointB = points[0]
                        tmp_dict['id'] = random_string()
                        tmp_dict['pointA'] = [pointA[0], pointA[1], section]
                        tmp_dict['pointB'] = [pointB[0], pointB[1], section]
                        tmp_dict['type'] = 'line'
                        tmp_dict['description'] = ""
                        data.append(tmp_dict)
            serializer = LineSerializer(data, many=True)
        return Response(serializer.data)

class Annotations(views.APIView):
    """
    Fetch UrlModel and return a set of two dictionaries. 
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
            .filter(active=True).filter(input_type_id__in=[1, 3, 5 , 6 , 7,4,11])\
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

    def get(self, request, brain_region, thresh):
        ontology_graph = make_ontology_graphCCFv3()

        neurons = self.mouselight_df.loc[self.mouselight_df['axonal_endpoint_dict'].apply(
            self.filter_by_region,args=(ontology_graph,brain_region,thresh,'ge'))]
        print(neurons)
        serializer = NeuronSerializer(neurons.to_records())
        return Response(serializer.data)

    def filter_by_region(self, dic, graph, allenID, thresh, operation):
        """ 
        Checks if dic[f'count_{allenID}'] (operation) thresh
        param: dic - dictionary where key in region ID and val is number of neurons with axonal endpoints in that region
        param: graph - ontology graph containing parent-child relationships between atlas regions 
        param: allenID - brain region ID to check
        param: thresh - a neuron with # of axonal endpoints above this thresh will be returned
        param: operation - can be one of 'ge', 'le', or 'eq'
        """
        dic = eval(dic) # turns json string into dict type
        # First get region name 
        allen_name = graph.lookup_region_name_by_id(allenID)
        # get all progeny (by name) 
        progeny_byname = graph.get_progeny(allen_name)
        all_regions_byid = [allenID] + [graph.get_id(name) for name in progeny_byname]
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
    urlModel = UrlModel.objects.get(pk=url_id).all()
    if urlModel.layers is not None:
        layers = urlModel.layers
    return render(request, 'layer_dropdown_list_options.html', {'layers': layers})

def public_list(request):
    """
    Shows a listing of urls made available to the public
    :param request:
    :return:
    """
    urls = UrlModel.objects.filter(public=True).order_by('comments')
    return render(request, 'public.html', {'urls': urls})

class LandmarkList(views.APIView):

    def get(self, request, format=None):

        list_of_landmarks = Structure.objects.all().filter(active = True).all()
        list_of_landmarks = [i.abbreviation for i in list_of_landmarks]
        data = {}
        data['land_marks'] = list_of_landmarks
        return JsonResponse(data)