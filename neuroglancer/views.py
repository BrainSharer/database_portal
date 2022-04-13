from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Q
import string
import random
import numpy as np
from scipy.interpolate import splprep, splev
from neuroglancer.serializers import AnnotationSerializer, \
    AnnotationsSerializer, NeuroglancerSerializer, NeuronSerializer, AnatomicalRegionSerializer, \
    ViralTracingSerializer
from neuroglancer.models import NeuroglancerModel, AnnotationPoints, MouselightNeuron, \
    ViralTracingLayer
from neuroglancer.atlas import get_scales, make_ontology_graph_CCFv3, make_ontology_graph_pma
    
from brain.models import BrainRegion

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
    def get(self, request, animal_id, label, format=None):
        data = []
        try:
            rows = AnnotationPoints.objects.filter(animal=animal_id)\
                        .filter(label=label)\
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
        layers = AnnotationPoints.objects.order_by('animal__animal_name', 'label')\
            .filter(label__isnull=False)\
            .values('animal__id', 'animal__animal_name', 'label')\
            .distinct()
        for layer in layers:
            data.append({
                "animal_id":layer['animal__id'],
                "animal_name":layer['animal__animal_name'],
                "label":layer['label'],
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

    """
    Fetch MouseLight neurons meeting filter criteria 
    url is of the the form
    mlneurons/<str:atlas_name>/<str:neuron_parts_boolstr>/<str:brain_region1>/<str:filter_type1>/<str:operator_type1>/<int:thresh1>/<str:filter_type2>/<str:operator_type2>/<int:thresh2>
    Where:
        atlas_name               <str> : required, either "ccfv3_25um" or "pma_20um"
        neuron_parts_boolstr     <str> : required, e.g. "true-true-false" denotes whether to fetch somata, axons and dendrites, respectively
        brain_region1            <str> : required, e.g. "Cerebellum"
        filter_type1             <str> : optional, e.g. "soma", "axon_endpoints", ...
        operator_type1           <str> : optional, e.g. "gte" -> "greater than or equal to"
        thresh1                  <int> : optional, e.g. 2 
        brain_region2            <str> : optional, e.g. "Thalamus"
        filter_type2             <str> : optional, e.g. "dendritic_branchpoints"
        operator_type2           <str> : optional, e.g. "eq" -> "exactly equal to"
        thresh2                  <int> : optional, e.g. 5
    """

    def get(self, request, atlas_name, neuron_parts_boolstr, brain_region1, 
        filter_type1='soma', operator_type1=None, thresh1=None,
        brain_region2=None, filter_type2=None, operator_type2=None, thresh2=None):
        
        print(atlas_name,brain_region1,filter_type1,
            operator_type1,thresh1,brain_region2,
            filter_type2,operator_type2,thresh2)
        
        if atlas_name == 'ccfv3_25um':
            ontology_graph = make_ontology_graph_CCFv3()
        elif atlas_name == 'pma_20um':
            ontology_graph = make_ontology_graph_pma()
        
        # filter to only get neurons in this atlas
        rows = MouselightNeuron.objects.filter(annotation_space__exact=atlas_name)
        all_ids_thisatlas = [x for x in rows.values_list('id',flat=True)]
        # Filter #1, required
        brain_region_id1 = ontology_graph.get_id(brain_region1)
        if filter_type1 == 'soma':
            # Figure out all progeny of this region since neuron could be in this shell or any child
            progeny = ontology_graph.get_progeny(brain_region1)
            progeny_ids = [ontology_graph.get_id(prog) for prog in progeny]
            ids_tosearch = [brain_region_id1] + progeny_ids
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

        neuron_indices = [all_ids_thisatlas.index(ID) for ID in rows.values_list('id',flat=True)]
        # Only add neuron parts we want
        # The "id" in the database describes the neuron id
        # Each neuron has a different skeleton for its soma, axon and dendrite
        # and we can choose which of them to fetch and display in neuroglancer
        # id itself corresponds to the soma  
        # id + 1 corresponds to the axon 
        # id + 2 corresponds to the dendrite
        somata_boolstr, axons_boolstr, dendrites_boolstr = neuron_parts_boolstr.split('-')
        neuron_parts_indices = []
        if somata_boolstr == 'true':
            neuron_parts_indices.append(0) 
        if axons_boolstr == 'true':
            neuron_parts_indices.append(1)
        if dendrites_boolstr == 'true':
            neuron_parts_indices.append(2)
        # make the list of skeleton ids to get based on our database ids as well as 
        # which parts of the neurons we were asked to get
        skeleton_segment_ids = [ix*3+x for ix in neuron_indices for x in neuron_parts_indices]
        serializer = NeuronSerializer({'segmentId':skeleton_segment_ids})
        return Response(serializer.data)

class AnatomicalRegions(views.APIView):
    """
    Fetch the complete list of anatomical brain regions
    url is of the the form
    /anatomicalregions/atlasName
    """
    print("In anatomical regions")
    def get(self, request, atlas_name):
        if atlas_name == 'ccfv3_25um':
            ontology_graph = make_ontology_graph_CCFv3()
        elif atlas_name == 'pma_20um':
            ontology_graph = make_ontology_graph_pma()
        segment_names = list(ontology_graph.graph.keys())
        serializer = AnatomicalRegionSerializer({'segment_names':segment_names})
        return Response(serializer.data)

class TracingAnnotation(views.APIView):
    """
    Fetch Viral tracing datasets meeting filter criteria 
    url is of the the form
    tracing_annotations/<str:virus_timepoint>/<str:primary_inj_site>
    Where:
        virus_timepoint   <str> : required, "HSV-H129_Disynaptic", "HSV-H129_Trisynaptic" or "PRV_Disynaptic"
        primary_inj_site  <str> : required, e.g. "Lob. I-V" 
    """
    def get(self, request, virus_timepoint, primary_inj_site):

        virus,timepoint = virus_timepoint.split("_")

        if primary_inj_site == 'All sites':
            rows = ViralTracingLayer.objects.filter(
                virus=virus,
                timepoint=timepoint)
        else:
            rows = ViralTracingLayer.objects.filter(
                virus=virus,
                timepoint=timepoint,
                primary_inj_site=primary_inj_site)

        brain_names = rows.values_list('brain_name',flat=True)
        brain_urls = [f'https://lightsheetatlas.pni.princeton.edu/public/tracing/{virus_timepoint}/{brain_name}_eroded_cells_no_cerebellum' \
            for brain_name in brain_names]
        
        # Make a dict to map inputs we receive to what the db fields expect
        primary_inj_site_dict = {
            "Lob. I-V":"lob_i_v",
            "Lob. VI, VII":"lob_vi_vii",
            "Lob. VIII-X":"lob_viii_x",
            "Simplex":"simplex",
            "Crus I":"crusi",
            "Crus II":"crusii",
            "PM, CP":"pm_cp",
            "All sites":"all"}
        
        primary_inj_site_fieldname = primary_inj_site_dict[primary_inj_site]

        # get fraction injected in primary site
        if primary_inj_site_fieldname == 'all': # then sites could be different for each brain 
            print("all injection sites")
            frac_injections = []
            primary_injection_sites = rows.values_list('primary_inj_site',flat=True)
            for ii,row in enumerate(rows):
                primary_injection_site = primary_injection_sites[ii]
                primary_inj_site_fieldname = primary_inj_site_dict[primary_injection_site]
                frac_injection = getattr(row,f'frac_inj_{primary_inj_site_fieldname}')
                # frac_injection =
                frac_injections.append(frac_injection)
        else:
            frac_injections = rows.values_list(f'frac_inj_{primary_inj_site_fieldname}')
            primary_injection_sites = [primary_inj_site for _ in frac_injections]

        serializer = ViralTracingSerializer({
            'brain_names':brain_names,
            'primary_inj_sites':primary_injection_sites,
            'frac_injections':frac_injections,
            'brain_urls':brain_urls})

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
    
    
