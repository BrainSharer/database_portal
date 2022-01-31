"""
These are methods taken from notebooks, mostly Bili's
There are constants defined in the models.py script and imported here
so we can resuse them througout the code.
"""
from authentication.models import User
import datetime
from brain.models import Animal, ScanRun, BrainRegion
from neuroglancer.models import AnnotationPoints, AnnotationPointArchive
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
from timeit import default_timer as timer
from neuroglancer.bulk_insert import BulkCreateManager
MANUAL = 1
DETECTED = 2



def get_centers_dict(animal_id, input_type_id=0, owner_id=None):
    '''
    This method is used to get data for the rigid transformation.
    :param animal_id:
    :param input_type_id:
    :param owner_id:
    '''
    rows = AnnotationPoints.objects.filter(animal=animal_id)\
        .filter(active=True).filter(layer='COM')
    if input_type_id > 0:
        rows = rows.filter(input_type_id=input_type_id)
    if owner_id is not None:
        rows = rows.filter(owner_id=owner_id)
    structure_dict = {}
    structures = BrainRegion.objects.filter(active=True).all()
    for structure in structures:
        structure_dict[structure.id] = structure.abbreviation
    row_dict = {}
    for row in rows:
        structure_id = row.structure_id
        abbreviation = structure_dict[structure_id]
        # do transform here.
        row_dict[abbreviation] = [row.x, row.y, row.section]
    return row_dict


def get_brain_region(annotation):
    '''
    This method gets a brain_region from the brain_region table. It used
    to be called structure. 
    It initially fetches the very first brain region just so it returns
    something. It then queries the table based on the abbreviation.
    :param annotation: is a json object that might contain a description key.
    '''
    brain_region = BrainRegion.objects.get(pk=1)
    if 'description' in annotation:
        abbreviation = str(annotation['description']).replace('\n', '').strip()
        try:
            brain_region = BrainRegion.objects.get(abbreviation=abbreviation)
        except BrainRegion.DoesNotExist:
            logger.error(f'Structure {abbreviation} does not exist')
    return brain_region

def move_annotations(animal, layer):
    '''
    Move existing annotations into the archive. First we get the existing
    rows and then we insert those into the archive table. This is rather
    expensive operation to perform as we're doing:
        1. a select of the existing rows.
        2. bulk inserts of those rows
        3. deleting those rows from the primary table
    :param animal: animal object
    :param layer: char of layer name
    TODO, we need to get the FK from the archive table
    '''
    rows = AnnotationPoints.objects.filter(input_type_id=MANUAL)\
        .filter(animal=animal)\
        .filter(layer=layer)
        
    bulk_mgr = BulkCreateManager(chunk_size=100)
    for row in rows:
        bulk_mgr.add(AnnotationPointArchive(animal=row.animal, brain_region=row.brain_region,
            layer=row.layer, owner=row.owner, input_type=row.input_type,
            x=row.x, y=row.y, z=row.z))
    bulk_mgr.done()
    # now delete them as they are no longer useful in the original table.
    rows.delete()

        

def bulk_annotations(animal, layer, loggedInUser, layer_name):
    '''
    This method takes in a json layer from neuroglancer, loops through
    it to find all the annotations and then for each layer, it loops
    though each annotation and adds to a bulk inserter.
    :param animal: object of the animal
    :param layer: json object of layer data
    :param loggedInUser: int of owner
    :param layer_name: str of the layer name
    '''
    bulk_mgr = BulkCreateManager(chunk_size=100)
    scale_xy, z_scale = get_scales(animal.id)
    annotations = layer['annotations']
    for annotation in annotations:
        x1 = annotation['point'][0] * scale_xy
        y1 = annotation['point'][1] * scale_xy
        z1 = annotation['point'][2] * z_scale
        brain_region = get_brain_region(annotation)
        if brain_region is not None and animal is not None and loggedInUser is not None:
            bulk_mgr.add(AnnotationPoints(animal=animal, brain_region=brain_region,
            layer=layer_name, owner=loggedInUser, input_type_id=MANUAL,
            x=x1, y=y1, z=z1))
    bulk_mgr.done()

def update_annotation_data(neuroglancerModel):
    '''
    This method is called by the Neuroglancer serializer, both in the update
    and in the create methods.
    It loops through all the layers and finds annotation data to insert.
    It will not insert annotation data that has the default name of 'annotation'.
    :param neuroglancerModel: object model of the neuroglancer state
    '''
    start = timer()
    json_txt = neuroglancerModel.neuroglancer_state
    try:
        # loggedInUser = User.objects.get(id=neuroglancerModel.owner.id)
        loggedInUser = neuroglancerModel.owner
    except User.DoesNotExist:
        logger.error("User does not exist")
        return
    try:
        animal = Animal.objects.get(animal=neuroglancerModel.animal)
    except Animal.DoesNotExist:
        logger.error("Animal does not exist")
        return
    if 'layers' in json_txt:
        layers = json_txt['layers']
        for layer in layers:
            if 'annotations' in layer:
                layer_name = str(layer['name']).strip()
                if layer_name != 'annotation':
                    move_annotations(animal, layer_name)
                    bulk_annotations(animal, layer, loggedInUser, layer_name)
    end = timer()
    print(f'Deleting and inserting data took {end - start} seconds')

def get_scales(animal_id):
    """
    A generic method to safely query and return resolutions
    param: animal_id integer of the primary key of the animal
    """
    try:
        query_set = ScanRun.objects.filter(animal=animal_id)
    except ScanRun.DoesNotExist:
        print('No scan run for', animal_id)
        scan_run = None
    if query_set is not None and len(query_set) > 0:
        scan_run = query_set[0]
        scale_xy = scan_run.resolution
        z_scale = scan_run.zresolution
    else:
        scale_xy = 1
        z_scale = 1
    print(scale_xy, z_scale)
    return scale_xy, z_scale
