"""
These are methods taken from notebooks, mostly Bili's
There are constants defined in the models.py script and imported here
so we can resuse them througout the code.
"""
import numpy as np
from django.contrib.auth.models import User
import datetime
from neuroglancer.models import Structure, LayerData, LAUREN_ID, \
    ATLAS_Z_BOX_SCALE
from brain.models import Animal, ScanRun
from abakit.registration.algorithm import umeyama
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
MANUAL = 1
CORRECTED = 2

monitored_layer_names = {'COM':'COM','ADDITIONAL MANUAL ANNOTATIONS':'COM_addition'}

def align_atlas(animal, input_type_id=None, person_id=None):
    """
    This prepares the data for the align_point_sets method.
    Make sure we have at least 3 points
    :param animal: the animal we are aligning to
    :param input_type_id: the int defining what type of input. Taken from the
    com_type table with  column=id
    :param person_id: the int defining the person. Taken from the auth_user
    table column=id
    :return: a 3x3 matrix and a 1x3 matrix
    """

    atlas_centers = get_centers_dict('atlas',
                                     input_type_id=MANUAL,
                                     person_id=LAUREN_ID)
    reference_centers = get_centers_dict(animal,
                                         input_type_id=input_type_id,
                                         person_id=person_id)
    try:
        scanRun = ScanRun.objects.get(prep__prep_id=animal)
    except ScanRun.DoesNotExist:
        scanRun = None

    if len(reference_centers) > 2 and scanRun is not None:
        resolution = scanRun.resolution
        reference_scales = (resolution, resolution, ATLAS_Z_BOX_SCALE)
        structures = sorted(reference_centers.keys())
        # align animal to atlas
        common_keys = atlas_centers.keys() & reference_centers.keys()
        dst_point_set = np.array([atlas_centers[s] for s in structures if s in common_keys]).T
        src_point_set = np.array([reference_centers[s] for s in structures if s in common_keys]).T
        R, t = umeyama(src_point_set, dst_point_set)
        t = t / np.array([reference_scales]).T # production version

    else:
        R = np.eye(3)
        t = np.zeros((3,1))
    return R, t

def get_centers_dict(prep_id, input_type_id=0, person_id=None):
    rows = LayerData.objects.filter(prep__prep_id=prep_id)\
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

def get_existing_structures(prep,loggedInUser,layer='COM',):
    existing_structures = set()
    existing_layer_data = LayerData.objects.filter(input_type_id=MANUAL)\
        .filter(prep=prep)\
        .filter(active=True)\
        .filter(person = loggedInUser)\
        .filter(layer=layer)\

    for s in existing_layer_data:
        existing_structures.add(s.structure.id)
    return existing_structures

def get_com_structure(com):
    abbreviation = str(com['description']).replace('\n', '').strip()
    structure = None
    try:
        structure = Structure.objects.get(abbreviation=abbreviation)
    except Structure.DoesNotExist:
        print(f'Structure {abbreviation} does not exist')
        logger.error("Structure does not exist")
    return structure

def update_com(prep,coordinates,structure,loggedInUser,layer = 'COM'):
    x,y,z = coordinates
    LayerData.objects.filter(input_type_id=MANUAL)\
        .filter(prep=prep)\
        .filter(active=True)\
        .filter(layer=layer)\
        .filter(structure=structure)\
        .update(x=x, y=y, section=z, 
                updatedby=loggedInUser, 
                updated=datetime.datetime.now())    

def add_com(prep,structure,coordinates,loggedInUser,layer = 'COM'):
    print(f'adding {structure}' )
    x,y,z = coordinates
    try:
        LayerData.objects.create(
            prep=prep, structure=structure, created=datetime.datetime.now(),
            layer = layer, active=True, person=loggedInUser, input_type_id=MANUAL,
            x=x, y=y, section=z)
    except Exception as e:
        logger.error(f'Error inserting manual {structure.abbreviation}', e)

def delete_com(prep,structure,loggedInUser,layer = 'COM'):
    LayerData.objects.filter(person=loggedInUser)\
    .filter(input_type_id=MANUAL)\
    .filter(prep=prep)\
    .filter(active=True)\
    .filter(layer=layer)\
    .filter(structure_id=structure)\
    .delete()

def update_or_insert_annotations(prep,layer,loggedInUser,existing_structures,layer_name = 'COM'):
    scale_xy, z_scale = get_scales(prep.prep_id)
    annotation = layer['annotations']
    for com in annotation:
        x = com['point'][0] * scale_xy
        y = com['point'][1] * scale_xy
        z = com['point'][2] * z_scale
        if 'description' in com:
            structure = get_com_structure(com)
            if structure is not None and prep is not None and loggedInUser is not None:
                if structure.id in existing_structures:
                    update_com(prep,(x,y,z),structure,loggedInUser,layer_name)
                    existing_structures.discard(structure.id)
                else:
                    add_com(prep,structure,(x,y,z),loggedInUser,layer_name)
    return existing_structures

def update_center_of_mass(urlModel):
    """
    This method checks if there is center of mass data. If there is,
    then it first find the center of mass rows for that
    person/input_type/animal/active combination.
    If data already exists for that combination above, it all gets set to
    inactive. Then the new data gets inserted. No updates!
    It does lots of checks to make sure it is in the correct format,
    including:
        layer must be named COM
        structure name must be in the description field
        structures must exactly match the structure names in the database,
        though this script does strip line breaks, white space off.
    :param urlModel: the long url from neuroglancer
    :return: nothing
    """
    json_txt = urlModel.url
    try:
        loggedInUser = User.objects.get(pk=urlModel.person.id)
    except User.DoesNotExist:
        logger.error("User does not exist")
        return
    try:
        prep = Animal.objects.get(pk=urlModel.animal)
    except Animal.DoesNotExist:
        logger.error("Animal does not exist")
        return
    if 'layers' in json_txt:
        layers = json_txt['layers']
        for layer in layers:
            if 'annotations' in layer:
                layer_name = str(layer['name']).upper().strip()
                if layer_name in monitored_layer_names:
                    layer_name = monitored_layer_names[layer_name]
                    existing_structures = get_existing_structures(prep,loggedInUser,layer_name)
                    remaining_structures = update_or_insert_annotations(prep,layer,loggedInUser,existing_structures,layer_name)
                    for structure in remaining_structures:
                        delete_com(prep,structure,loggedInUser,layer_name)


def get_scales(prep_id):
    """
    A generic method to safely query and return resolutions
    param: prep_id varchar of the primary key of the animal
    """
    try:
        query_set = ScanRun.objects.filter(prep_id=prep_id)
    except ScanRun.DoesNotExist:
        scan_run = None
    if query_set is not None and len(query_set) > 0:
        scan_run = query_set[0]
        scale_xy = scan_run.resolution
        z_scale = ATLAS_Z_BOX_SCALE
    else:
        scale_xy = 1
        z_scale = 1
    return scale_xy, z_scale
