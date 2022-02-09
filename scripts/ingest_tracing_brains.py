import os, sys, glob, json
import pandas as pd
from datetime import datetime
from functools import lru_cache


HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'brainsharer')
sys.path.append(PATH)
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brainsharer.settings")
import django
django.setup()

from neuroglancer.models import ViralTracingLayer

if __name__ == '__main__':
    tracing_spreadsheet = os.path.join(PATH,'static/neuroglancer',
        'pisano2021_brains_metadata_simple_with_injection_fractions.csv')
    df = pd.read_csv(tracing_spreadsheet)
    print(df)
    insert_list = []
    for ii,row in df.iterrows():
        print(ii)
        brain_name = row['brain']
        virus = row['virus']
        timepoint = row['timepoint'].split()[0]
        primary_inj_site = row['primary injection site']
        frac_inj_lob_i_v = row['Lob. I-V']
        frac_inj_lob_vi_vii = row['Lob. VI, VII']
        frac_inj_lob_viii_x = row['Lob. VIII-X']
        frac_inj_simplex = row['Simplex']
        frac_inj_crusi = row['Crus I']
        frac_inj_crusii = row['Crus II']
        frac_inj_pm_cp = row['PM, CP']
        
        obj = ViralTracingLayer(
            id=ii+1,
            brain_name = brain_name,
            virus = virus,
            timepoint = timepoint,
            primary_inj_site = primary_inj_site,
            frac_inj_lob_i_v = frac_inj_lob_i_v,
            frac_inj_lob_vi_vii = frac_inj_lob_vi_vii,
            frac_inj_lob_viii_x = frac_inj_lob_viii_x,
            frac_inj_simplex = frac_inj_simplex,
            frac_inj_crusi = frac_inj_crusi,
            frac_inj_crusii = frac_inj_crusii,
            frac_inj_pm_cp = frac_inj_pm_cp
        )
        insert_list.append(obj)
    ViralTracingLayer.objects.bulk_create(insert_list)
    # ViralTracingLayer.objects.bulk_update(insert_list,
    #     ['frac_inj_lob_i_v','frac_inj_lob_vi_vii','frac_inj_lob_viii_x',
    #     'frac_inj_simplex','frac_inj_crusi','frac_inj_crusii','frac_inj_pm_cp'])
    # ViralTracingLayer.objects.bulk_update(insert_list,
    #     ['timepoint'])


    print("Worked")




                
        


