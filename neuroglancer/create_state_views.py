from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import os
from brain.models import Animal

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

