import os, sys
import argparse
import numpy as np
import pandas as pd

HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'programming/activebrainatlas')
sys.path.append(PATH)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activebrainatlas.settings")
import django
from django.db import connection
django.setup()

from neuroglancer.models import LayerData, ANNOTATION_ID
from neuroglancer.atlas import get_atlas_centers, get_brain_coms, get_common_structures

def prepare_table_for_save(brains, common_structures, person_id, input_type_id):
    brain_coms = get_brain_coms(brains, person_id, input_type_id)
    atlas_coms = get_atlas_centers()

    data = {}
    data['name'] = []
    for s in common_structures:
        for c in ['dx', 'dy', 'dz', 'dist']:
            data['name'] += [f'{s}_{c}']
    for brain in brain_coms.keys():
        data[brain] = []
        offset = [brain_coms[brain][s] - atlas_coms[s]
                  if s in brain_coms[brain] else [np.nan, np.nan, np.nan]
                  for s in common_structures]
        offset = np.array(offset)
        scale = np.array([10, 10, 20])
<<<<<<< HEAD
        scale = np.array([1,1,1])
=======
<<<<<<< HEAD
=======
        scale = np.array([1,1,1])
>>>>>>> 2506b46b783fcb79b7a2a01c72870d13be9b69fb
>>>>>>> df84383e5889ddcc6c968a873eda1b067e4270e2
        dx, dy, dz = (offset * scale).T
        dist = np.sqrt(dx * dx + dy * dy + dz * dz)
        for dx_i, dy_i, dz_i, dist_i in zip(dx, dy, dz, dist):
            data[brain] += [dx_i, dy_i, dz_i, dist_i]
    return pd.DataFrame(data)


def test_com():
  brains = list(LayerData.objects.filter(active=True)\
      .filter(input_type__input_type__in=['manual'])\
      .filter(layer='COM')\
      .filter(active=True)\
<<<<<<< HEAD
      .exclude(prep_id__in=['Atlas','MD589','DK46'])\
=======
<<<<<<< HEAD
      .exclude(prep_id='Atlas')\
=======
      .exclude(prep_id__in=['Atlas','MD589','DK46'])\
>>>>>>> 2506b46b783fcb79b7a2a01c72870d13be9b69fb
>>>>>>> df84383e5889ddcc6c968a873eda1b067e4270e2
      .values_list('prep_id', flat=True).distinct().order_by('prep_id'))
  print(brains)
  atlas_coms = get_atlas_centers()
  common_structures = get_common_structures(brains)
  print(common_structures)
  # 28 is Bili
  # input_type_id = aligned
  df = prepare_table_for_save(brains, common_structures, person_id=28, input_type_id=4)
  print(df.head())





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on Animal')
    test_com()

