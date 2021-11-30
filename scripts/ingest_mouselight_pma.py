import os, sys, glob, json
import pandas as pd
from datetime import datetime
from functools import lru_cache


HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'Git/brainsharer/database_portal')
sys.path.append(PATH)
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brainsharer.settings")
import django
django.setup()

from neuroglancer.atlas import make_ontology_graph_pma
from neuroglancer.models import MouselightNeuron

@lru_cache
def memo_get_id(region_name):
    return ontology_graph.get_id(region_name)

@lru_cache
def memo_lookup_region_name_by_id(ID):
    return ontology_graph.lookup_region_name_by_id(ID)

@lru_cache
def memo_get_progenitors(region_name):
    return ontology_graph.get_progenitors(region_name)

def make_insert(neuron,ontology_graph,debug=False):
    # Make directory if it does not exist already
    neuron_name = neuron['idString']
    ### Soma
    soma = neuron['soma']
    
    ### Axon
    axon = neuron['axon']
    axon_branches_dict = {}
    axon_endpoints_dict = {}
    for pt_index,pt in enumerate(axon):
        sample_number = pt['sampleNumber']-1
        parent_number = pt['parentNumber']-1
        if parent_number >= 0:
            # Have to deal with axon splits and endpoints
            if (sample_number != parent_number + 1):
                # then the parent is at a branch split and child is at an endpoint
                atlas_id = pt['pmaId']
                atlas_id_parent = axon[pt_index-1]['pmaId']
                if atlas_id:
                    # figure out progenitor regions in the atlas and update those counts in the dicts too
                    cur_node_region_name = memo_lookup_region_name_by_id(atlas_id)
                    try:
                        cur_node_progenitors = memo_get_progenitors(cur_node_region_name)
                    except:
                        cur_node_progenitors = []

                    cur_node_atlas_ids = [atlas_id] + [memo_get_id(region_name) for region_name in cur_node_progenitors]

                    for cur_node_atlas_id in cur_node_atlas_ids:
                        try:
                            axon_endpoints_dict[f'count_{cur_node_atlas_id}'] += 1
                        except:
                            axon_endpoints_dict[f'count_{cur_node_atlas_id}'] = 1
                    
                if atlas_id_parent:
                    parent_node_region_name = memo_lookup_region_name_by_id(atlas_id_parent)
                    try:
                        parent_node_progenitors = memo_get_progenitors(parent_node_region_name)
                    except:
                        parent_node_progenitors = []
                    parent_node_atlas_ids = [atlas_id_parent] + [memo_get_id(region_name) for region_name in parent_node_progenitors]

                    for parent_node_atlas_id in parent_node_atlas_ids:
                        try:
                            axon_branches_dict[f'count_{parent_node_atlas_id}'] +=1
                        except: 
                            axon_branches_dict[f'count_{parent_node_atlas_id}'] = 1
                    
    ### Dendrite
    dendrite = neuron['dendrite']
    dendrite_branches_dict = {}
    dendrite_endpoints_dict = {}
    for pt_index,pt in enumerate(dendrite):
        sample_number = pt['sampleNumber']-1
        parent_number = pt['parentNumber']-1
        if parent_number >= 0:
            # Have to deal with dendrite splits and endpoints
            if (sample_number != parent_number + 1):
                # then the parent is at a branch split and child is at an endpoint
                atlas_id = pt['pmaId']
                atlas_id_parent = dendrite[pt_index-1]['pmaId']

                if atlas_id:
                    # figure out progenitor regions in the atlas and update those counts in the dicts too
                    cur_node_region_name = memo_lookup_region_name_by_id(atlas_id)
                    try:
                        cur_node_progenitors = memo_get_progenitors(cur_node_region_name)
                    except:
                        cur_node_progenitors = []

                    cur_node_atlas_ids = [atlas_id] + [memo_get_id(region_name) for region_name in cur_node_progenitors]

                    for cur_node_atlas_id in cur_node_atlas_ids:
                        try:
                            dendrite_endpoints_dict[f'count_{cur_node_atlas_id}'] += 1
                        except:
                            dendrite_endpoints_dict[f'count_{cur_node_atlas_id}'] = 1
                    
                if atlas_id_parent:
                    parent_node_region_name = memo_lookup_region_name_by_id(atlas_id_parent)
                    try:
                        parent_node_progenitors = memo_get_progenitors(parent_node_region_name)
                    except:
                        parent_node_progenitors = []
                    parent_node_atlas_ids = [atlas_id_parent] + [memo_get_id(region_name) for region_name in parent_node_progenitors]

                    for parent_node_atlas_id in parent_node_atlas_ids:
                        try:
                            dendrite_branches_dict[f'count_{parent_node_atlas_id}'] +=1
                        except: 
                            dendrite_branches_dict[f'count_{parent_node_atlas_id}'] = 1
                
    if soma['pmaId']:
        soma_atlas_id = soma['pmaId']
    else:
        soma_atlas_id = None
        
    obj = MouselightNeuron(
        idstring = neuron['idString'],
        sample_date = datetime.strptime(neuron['sample']['date'],"%Y-%m-%dT%H:%M:%S.%fZ"),
        sample_strain = neuron['sample']['strain'],
        virus_label = neuron['label']['virus'],
        fluorophore_label = neuron['label']['fluorophore'],
        annotation_space = "pma_20um",
        soma_atlas_id=soma_atlas_id,
        axon_endpoints_dict = axon_endpoints_dict,
        axon_branches_dict = axon_branches_dict,
        dendrite_endpoints_dict = dendrite_endpoints_dict,
        dendrite_branches_dict = dendrite_branches_dict)
    return obj

if __name__ == '__main__':
    ontology_graph = make_ontology_graph_pma()
    neuron_dir = '/home/ahoag/progs/mouselight/public/jsonPMA'
    json_files = sorted(glob.glob(neuron_dir + '/*json'))
    insert_list = []
    for neuron_json_file in json_files:
        print(neuron_json_file[-10:])
        with open(neuron_json_file,'r') as infile:
            neuron_data = json.load(infile)
        neuron = neuron_data['neuron']
        obj = make_insert(neuron,ontology_graph)
        insert_list.append(obj)
    MouselightNeuron.objects.bulk_create(insert_list,ignore_conflicts=True)

    # print(MouselightNeuron.)
    # MouselightNeuron.objects.create(
    #     idstring=subdf.idstring[0],
    #     axonal_endpoint_dict=subdf.axonal_endpoint_dict[0])
    print("Worked")




                
        


