import os, sys
import argparse
import pandas as pd
import datetime
from collections import defaultdict
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
Image.MAX_IMAGE_PIXELS = None

HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'programming/activebrainatlas')
sys.path.append(PATH)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activebrainatlas.settings")
import django
django.setup()

from neuroglancer.models import ANNOTATION_ID, LayerData



def parse_data(animal):
    CSV_PATH = f'/net/birdstore/Active_Atlas_Data/data_root/atlas_data/{animal}'
    csvfile = 'cshl2dk.aligned.csv'
    csvpath = os.path.join(CSV_PATH, csvfile)
    df = pd.read_csv(csvpath, names=['x','y','section'], header='infer')
    df = df.apply(pd.to_numeric) # convert all columns of DataFrame
    NOW = datetime.datetime.utcnow().isoformat()
    for index, row in df.iterrows():
        section = row['section'] * 20
        x = row['x'] * 0.325
        y = row['y'] * 0.325
        LayerData.objects.create(prep_id=animal, structure_id=ANNOTATION_ID, 
            layer='predicted_premotor', person_id=1,input_type_id=2,created=NOW, updated=NOW,
            x=x,y=y,section=section)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on Animal')
    parser.add_argument('--animal', help='Enter animal', required=True)
    args = parser.parse_args()

    animal = args.animal
    parse_data(animal)

