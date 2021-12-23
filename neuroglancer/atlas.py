"""
These are methods taken from notebooks, mostly Bili's
There are constants defined in the models.py script and imported here
so we can resuse them througout the code.
"""
from authentication.models import User
import datetime
from brain.models import Animal, ScanRun
from neuroglancer.models import Structure, AnnotationPoints
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
from timeit import default_timer as timer
from neuroglancer.bulk_insert import BulkCreateManager
MANUAL = 1
DETECTED = 2



def get_centers_dict(animal, input_type_id=0, person_id=None):
    rows = AnnotationPoints.objects.filter(animal__animal=animal)\
        .filter(active=True).filter(layer='COM')\
            .order_by('structure', 'updated')
    if input_type_id > 0:
        rows = rows.filter(input_type_id=input_type_id)
    if person_id is not None:
        rows = rows.filter(person_id=person_id)
    structure_dict = {}
    structures = Structure.objects.filter(active=True).all()
    for structure in structures:
        structure_dict[structure.id] = structure.abbreviation
    row_dict = {}
    for row in rows:
        structure_id = row.structure_id
        abbreviation = structure_dict[structure_id]
        # do transform here.
        row_dict[abbreviation] = [row.x, row.y, row.section]
    return row_dict


def get_existing_annotations(prep, loggedInUser, layer):
    existing_annotations = set()
    existing_layer_data = AnnotationPoints.objects.filter(input_type_id=MANUAL)\
        .filter(prep=prep)\
        .filter(active=True)\
        .filter(person=loggedInUser)\
        .filter(layer=layer)\

    for s in existing_layer_data:
        existing_annotations.add(s.id)
    return existing_annotations


def get_structure(annotation):
    structure = Structure.objects.get(pk=1)
    if 'description' in annotation:
        abbreviation = str(annotation['description']).replace('\n', '').strip()
        try:
            structure = Structure.objects.get(abbreviation=abbreviation)
        except Structure.DoesNotExist:
            logger.error(f'Structure {abbreviation} does not exist')
    return structure


def update_annotation(prep, coordinates, structure, loggedInUser, layer='COM'):
    x, y, z = coordinates
    AnnotationPoints.objects.filter(input_type_id=MANUAL)\
        .filter(prep=prep)\
        .filter(active=True)\
        .filter(layer=layer)\
        .filter(structure=structure)\
        .update(x=x, y=y, section=z,
                updatedby=loggedInUser,
                updated=datetime.datetime.now())    


def add_annotation(animal, structure, coordinates, loggedInUser, layer='COM'):
    x, y, z = coordinates
    try:
        AnnotationPoints.objects.create(
            animal=animal, structure=structure,
            layer=layer, owner=loggedInUser, input_type_id=MANUAL,
            x=x, y=y, section=z)
    except Exception as e:
        logger.error(f'Error inserting manual {structure.abbreviation}', e)


def delete_annotations(animal, loggedInUser, layer):
    AnnotationPoints.objects.filter(animal=loggedInUser)\
    .filter(input_type_id=MANUAL)\
    .filter(animal=animal)\
    .filter(layer=layer)\
    .delete()


def insert_annotations(animal, layer, loggedInUser, layer_name):
    scale_xy, z_scale = get_scales(animal.animal)
    annotations = layer['annotations']
    for annotation in annotations:
        x = annotation['point'][0] * scale_xy
        y = annotation['point'][1] * scale_xy
        z = annotation['point'][2] * z_scale
        structure = get_structure(annotation)
        if structure is not None and animal is not None and loggedInUser is not None:
            add_annotation(animal, structure, (x, y, z), loggedInUser, layer_name)

def bulk_annotations(animal, layer, loggedInUser, layer_name):
    bulk_mgr = BulkCreateManager(chunk_size=100)
    scale_xy, z_scale = get_scales(animal.animal)
    annotations = layer['annotations']
    for annotation in annotations:
        x1 = annotation['point'][0] * scale_xy
        y1 = annotation['point'][1] * scale_xy
        z1 = annotation['point'][2] * z_scale
        structure = get_structure(annotation)
        if structure is not None and animal is not None and loggedInUser is not None:
            bulk_mgr.add(AnnotationPoints(animal=animal, structure=structure,
            layer=layer_name, owner=loggedInUser, input_type_id=MANUAL,
            x=x1, y=y1, section=z1))
    bulk_mgr.done()

def update_annotation_data(neuroglancerModel):
    """
    Delete existing data then insert
    """
    start = timer()
    json_txt = neuroglancerModel.neuroglancer_state
    try:
        loggedInUser = User.objects.get(pk=neuroglancerModel.owner.id)
    except User.DoesNotExist:
        logger.error("User does not exist")
        return
    try:
        prep = Animal.objects.get(animal=neuroglancerModel.animal)
    except Animal.DoesNotExist:
        logger.error("Animal does not exist")
        return
    if 'layers' in json_txt:
        layers = json_txt['layers']
        for layer in layers:
            if 'annotations' in layer:
                layer_name = str(layer['name']).strip()
                delete_annotations(prep, loggedInUser, layer_name)
                bulk_annotations(prep, layer, loggedInUser, layer_name)
    end = timer()
    print(f'Deleting and inserting data took {end - start} seconds')

def get_scales(animal):
    """
    A generic method to safely query and return resolutions
    param: animal varchar of the primary key of the animal
    """
    try:
        query_set = ScanRun.objects.filter(animal=animal)
    except ScanRun.DoesNotExist:
        scan_run = None
    if query_set is not None and len(query_set) > 0:
        scan_run = query_set[0]
        scale_xy = scan_run.resolution
        z_scale = scan_run.zresolution
    else:
        scale_xy = 1
        z_scale = 1
    return scale_xy, z_scale
