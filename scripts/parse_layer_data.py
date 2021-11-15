import os, sys
import argparse
import pandas as pd

HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'programming/activebrainatlasadmin')
sys.path.append(PATH)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activebrainatlas.settings")
import django
django.setup()

from neuroglancer.models import UrlModel



def parse_layer(id):
  data = UrlModel.objects.get(pk=id)
  json_txt = data.url
  layers = json_txt['layers']
  for layer in layers:
      if 'annotations' in layer:
          name = layer['name']
          annotation = layer['annotations']
          d = [row['point'] for row in annotation if 'point' in row]
          print(d)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on Animal')
    parser.add_argument('--id', help='Enter ID', required=True)

    args = parser.parse_args()
    id = int(args.id)
    parse_layer(id)

