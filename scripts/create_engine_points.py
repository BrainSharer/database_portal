import os, sys
import argparse

HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'programming/activebrainatlas')
sys.path.append(PATH)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activebrainatlas.settings")
import django
from django.db import connection
django.setup()

from neuroglancer.models import LayerData, ANNOTATION_ID



def create_layer(animal, id, start, debug):

    with connection.cursor() as cursor:
        sql = """select el.id, el.frame, el.points, elab.name 
                from engine_labeledshape el  
                inner join engine_label elab on el.label_id = elab.id
                where elab.task_id = %s 
                order by elab.name, el.frame"""
        cursor.execute(sql, [id])
        rows = cursor.fetchall()
    count = 1
    for row in rows:
        id = row[0]
        section = row[1] + start
        points = row[2]
        layer = row[3]
        s = points.split(',')
        points = map(','.join, zip(s[::2], s[1::2]))
        p = 0
        for point in points:
            x,y = point.split(',')
            x = float(x)
            y = float(y)
            x *= 32
            y *= 32
            if debug:
                print(count, id, animal, ANNOTATION_ID, layer, x,y,section)
                count += 1
            else:
                LayerData.objects.create(prep_id=animal, segment_id=id, structure_id = ANNOTATION_ID, person_id=1,
                                                layer=layer, input_type_id = 5,
                                                x=x,y=y,section=section)    
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on Animal')
    parser.add_argument('--id', help='Enter ID', required=True)
    parser.add_argument('--animal', help='Enter animal', required=True)    
    parser.add_argument('--start', help='Enter start', required=True)
    parser.add_argument('--debug', help='Enter debug True|False', required=False, default='false')

    args = parser.parse_args()
    animal = args.animal
    id = int(args.id)
    start = int(args.start)
    debug = bool({'true': True, 'false': False}[str(args.debug).lower()])
    create_layer(animal, id, start, debug)




                
"""
json for line:
{
          "id": "6ce1a6e0b25292ed7d95abc19e29beaf61471718",
          "pointA": [
            23453.7265625,
            6428.55322265625,
            236.49998474121094
          ],
          "pointB": [
            25050.107421875,
            11495.3271484375,
            236.49998474121094
          ],
          "type": "line"
        },
json for point
{
          "id": "c6f81a41abdcf7d6b419a3353b982abc03e0a37e",
          "point": [
            47751.0859375,
            21584.93359375,
            276.5000305175781
          ],
          "type": "point"
        }
 """       


