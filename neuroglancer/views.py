from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework.response import Response
from django.http import Http404
import string
import random
import numpy as np
from scipy.interpolate import splprep, splev
from neuroglancer.serializers import AnnotationSerializer, \
    AnnotationsSerializer, NeuroglancerSerializer
from neuroglancer.models import InputType, NeuroglancerModel, AnnotationPoints
from brain.models import BrainRegion
from neuroglancer.atlas import get_scales

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)


class NeuroglancerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the neuroglancer states to be viewed or edited.
    Note, the update, and insert methods are over riden in the serializer.
    It was more convienent to do them there than here.
    """
    queryset = NeuroglancerModel.objects.all()
    serializer_class = NeuroglancerSerializer
    permission_classes = [permissions.AllowAny]

class Annotation(views.APIView):
    """
    Fetch AnnotationPoints model and return parsed annotation layer.
    neuroglancer is of the the form
    https://www.brainsharer.org/brainsharer/annotation/X/premotor/2
    Where:
         X is the PK integer of the animal (id),
         premotor is the label name,
         2 is the input type ID
    """
    def get(self, request, animal_id, label, FK_input_id, format=None):
        data = []
        try:
            rows = AnnotationPoints.objects.filter(animal=animal_id)\
                        .filter(label=label)\
                        .filter(input_type__id=FK_input_id)\
                        .order_by('z', 'id').all()
        except AnnotationPoints.DoesNotExist:
            raise Http404
        scale_xy, z_scale = get_scales(animal_id)
        for row in rows:
            point_dict = {}
            point_dict['type'] = 'point'
            point_dict['id'] = random_string()
            point_dict['point'] = \
                [int(round(row.x/scale_xy)), int(round(row.y/scale_xy)), int(round(row.z/z_scale))]
            point_dict['description'] = ""
            data.append(point_dict)
        serializer = AnnotationSerializer(data, many=True)
        return Response(serializer.data)

class Annotations(views.APIView):
    """
    Fetch NeuroglancerModel and return a set of two dictionaries. 
    One is from the layer_data
    table and the other is the COMs that have been set as transformations.
    {'id': 213, 'description': 'DK39 COM Test', 'label': 'COM'}
    url is of the the form:
    https://www.brainsharer.org/brainsharer/annotations
    """

    def get(self, request, format=None):
        """
        This will get the layer_data
        """
        data = []
        layers = AnnotationPoints.objects.order_by('animal', 'label', 'input_type__input_type')\
            .filter(label__isnull=False)\
            .values('animal', 'animal__animal', 'label','input_type__input_type','input_type__id')\
            .distinct()
        for layer in layers:
            data.append({
                "animal_id":layer['animal'],
                "animal_name":layer['animal__animal'],
                "label":layer['label'],
                "input_type":layer['input_type__input_type'],
                "FK_input_id":layer['input_type__id'],                
                })

        serializer = AnnotationsSerializer(data, many=True)
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

def random_string():
    '''
    This mimics the ID that neuroglancer creates as the ID for each annotation
    '''
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

        list_of_landmarks = BrainRegion.objects.all().filter(active = True).all()
        list_of_landmarks = [i.abbreviation for i in list_of_landmarks]
        data = {}
        data['land_marks'] = list_of_landmarks
        return JsonResponse(data)
    
    
