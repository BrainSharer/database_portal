from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import os
from brain.models import Animal, ScanRun
from authentication.models import User
from neuroglancer.models import NeuroglancerModel
from datetime import datetime

def fetch_layers(request, animal_id):
    print('animal is ', animal_id)
    animal = Animal.objects.get(pk=animal_id)
    url = animal.lab.lab_url
    if 'ucsd' in url.lower():
        url += f'/{animal.animal}/neuroglancer_data/' 
    else:
        url += animal.animal
    directories = read_url(url, ext="C")
    datarows = create_layer_table(animal.animal, directories)
    return render(request, 'layer_table.html',{'datarows': datarows})

def create_layer_table(animal, directories):
    layers = []
    for directory in directories:
        layer_name = os.path.basename(os.path.normpath(directory))
        if layer_name == animal:
            continue
        layer = {}
        layer['animal'] = animal
        layer['name'] = layer_name
        layer['source'] = f"{directory}"
        layer['type'] = get_layer_type(directory)
        layers.append(layer)
    return layers

def read_url(url, ext='', params={}):
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    directories = [url + node.get('href') for node in soup.find_all('a') 
              if '?' not in node.get('href')
              and node.get('href') != "/"]
    return directories


def get_layer_type(url):
    data_type = "NA"
    try:
        url += "info"
        response = requests.get(url)
        response.raise_for_status()
        info = response.json()
        if '@type' in info:
            data_type = info['@type']
        else:
            data_type = info['type']

    except Exception as err:
        print(f'Got error: {err}')
    
    return data_type

        
def prepare_top_attributes(layer):
    # {'id': 9, 'prep_id': 'DK39', 'lab': 'UCSD', 'description': 'C3', 'url': 'https://activebrainatlas.ucsd.edu/data/DK39/neuroglancer_data/C3', 'active': True, 'created': '2022-04-15T00:48:11', 'updated': '2022-04-15T14:48:11'}

    prep_id = layer['prep_id']
    visible_layer = 'C1'
    state = {}
    # animal
    try:
        query_set = Animal.objects.filter(animal_name=prep_id)
    except Animal.DoesNotExist:
        return state
    if query_set is not None and len(query_set) > 0:
        animal = query_set[0]

    try:
        query_set = ScanRun.objects.filter(animal=animal)
    except ScanRun.DoesNotExist:
        return state
    if query_set is not None and len(query_set) > 0:
        scan_run = query_set[0]
    
    state['dimensions'] = {'x':[scan_run.resolution, 'um'],
                            'y':[scan_run.resolution, 'um'],
                            'z':[scan_run.zresolution, 'um'] }
    state['position'] = [scan_run.width / 2, scan_run.height / 2, 225]
    state['selectedLayer'] = {'visible': True, 'layer': visible_layer}
    state['crossSectionScale'] = 90
    state['projectionScale'] = scan_run.width
    return state

def prepare_bottom_attributes():
    state = {}
    state['gpuMemoryLimit'] = 4000000000
    state['systemMemoryLimit'] = 8000000000
    state['layout'] = '4panel'
        
    return state
        
        
def create_layer(state):
    layer_name = state['description']
    url = state['url']
    layer = {}
    shaders = {}
    shaders['C1'] = '#uicontrol invlerp normalized\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n\nvoid main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n  \t  emitGrayscale(pix) ;\n}'
    shaders['C2'] = '#uicontrol invlerp normalized  (range=[0,45000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour) {\n  \t   emitRGB(vec3(pix,0,0));\n  \t} else {\n  \t  emitGrayscale(pix) ;\n  \t}\n\n}\n'
    shaders['C3'] = '#uicontrol invlerp normalized  (range=[0,5000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour){\n       emitRGB(vec3(0, (pix),0));\n    } else {\n      emitGrayscale(pix) ;\n    }\n\n}\n'
    layer['name'] = layer_name
    layer['shader'] = shaders.get(layer_name, 'C1')
    layer['source'] = f'precomputed://{url}'
    layer['type'] = 'image'
    layer['visible'] = True
    
    return layer
        
def create_neuroglancer_model(state):

    owner = User.objects.first()

    neuroglancer_state = NeuroglancerModel.objects.create(owner=owner, neuroglancer_state=state,
        created=datetime.now(), updated=datetime.now(), user_date="999999", 
        comments="XXXX", readonly=True)
    return neuroglancer_state.id