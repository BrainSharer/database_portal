import os, sys
import argparse

HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'programming/activebrainatlas')
sys.path.append(PATH)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activebrainatlas.settings")
import django
django.setup()

from neuroglancer.models import UrlModel, LayerData

def create_layer(layer_name, debug, id):

    if id is not None and id > 0:
        urlModel = UrlModel.objects.get(pk=id)
        urlModels = [urlModel]
    else:
        urlModels = UrlModel.objects.filter(vetted=True)
    inserts = 0
    data = {}
    for urlModel in urlModels:
        json_txt = urlModel.url
        layers = json_txt['layers']
        for layer in layers:
            if 'annotations' in layer:
                name = layer['name']
                if layer_name.lower() == str(name).lower():
                    annotation = layer['annotations']
                    points = [(row['id'], row['point']) for row in annotation]
                    for point in points:
                        id = point[0]
                        x,y,z = point[1]
                        section = int(z)
                        animal = urlModel.comments[0:4]
                        insert_name = name.capitalize()
                        if debug:
                            print(animal, urlModel.id, insert_name ,x,y,z,section)
                        else:
                            inserts += 1
                            LayerData.objects.create(prep_id=animal, url_id=urlModel.id, 
                                layer=insert_name,
                                x=x,y=y,section=section)

    print(f'Finished. Inserted {inserts} rows')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on Animal')
    parser.add_argument('--id', help='Enter URL ID', required=False)
    parser.add_argument('--layer', help='Enter layer name', required=True)
    parser.add_argument('--debug', help='Enter debug True|False', required=False, default='false')

    args = parser.parse_args()
    layer = args.layer
    id = args.id
    if id is not None:
        id = int(id)
    debug = bool({'true': True, 'false': False}[str(args.debug).lower()])
    create_layer(layer, debug, id)




                
        


