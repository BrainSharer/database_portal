from django.http import JsonResponse
from bs4 import BeautifulSoup
from brain.models import ScanRun
import requests
import json
import os

def createLayer(request, layer):
    data = {}
    data['layer'] = layer
    return JsonResponse(data)

def createAnimalLayer(request, animal):
    state = {}
    url = f"https://activebrainatlas.ucsd.edu/data/{animal}/neuroglancer_data/"
    scan_run = ScanRun.objects.get(prep__prep_id=animal)
    state["dimensions"] = {"x":[scan_run.resolution, "um"],
                           "y":[scan_run.resolution, "um"],
                           "z":[scan_run.zresolution, "um"] }
    state["position"] = [scan_run.width / 2, scan_run.height / 2, 225]
    state["projectionScale"] = scan_run.width

    directories = read_url(url, ext="C")
    layers = create_layers(directories)
    state["layers"] = layers
    print(json.dumps(state))
    return JsonResponse(state)

def create_layers(directories):
    layers = []
    shaders = {}
    shaders[0] = "#uicontrol invlerp normalized\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n\nvoid main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n  \t  emitGrayscale(pix) ;\n}"
    shaders[1] = "#uicontrol invlerp normalized  (range=[0,45000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour) {\n  \t   emitRGB(vec3(pix,0,0));\n  \t} else {\n  \t  emitGrayscale(pix) ;\n  \t}\n\n}\n"
    shaders[2] = "#uicontrol invlerp normalized  (range=[0,5000])\n#uicontrol float gamma slider(min=0.05, max=2.5, default=1.0, step=0.05)\n#uicontrol bool colour checkbox(default=true)\n\n  void main() {\n    float pix =  normalized();\n    pix = pow(pix,gamma);\n\n    if (colour){\n       emitRGB(vec3(0, (pix),0));\n    } else {\n      emitGrayscale(pix) ;\n    }\n\n}\n"
    for i, directory in enumerate(directories):
        layer_name = os.path.basename(os.path.normpath(directory))
        layer = {}
        layer["name"] = layer_name
        layer["shader"] = shaders.get(i, 0)
        layer["source"] = f"precomputed://{directory}"
        layer["type"] = "image"
        layer["visible"] = True
        layers.append(layer)
    return layers

def read_url(url, ext='', params={}):
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + node.get('href') for node in soup.find_all('a') 
              if node.get('href').startswith(ext)]
    return parent
