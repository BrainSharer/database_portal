import os, sys
import argparse
import numpy as np
from scipy.interpolate import UnivariateSpline,splprep, splev

HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'programming/activebrainatlas')
sys.path.append(PATH)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activebrainatlas.settings")
import django
from django.db import connection
django.setup()

from neuroglancer.models import LayerData, ANNOTATION_ID

def create_volume(str_contour, structure, color):
    """
    Takes in the contours of a structure as well as the name, sections spanned by the structure, and a list of
    parameters that dictate how it is rendered.
    Returns the binary structure volume.
    """
    sections = list(str_contour.keys())

    xy_ng_resolution_um = 10
    color_radius = 3
    xy_ng_resolution_um = xy_ng_resolution_um  # X and Y voxel length in microns
    color_radius = color_radius * (10.0 / xy_ng_resolution_um) ** 0.5
    first_sec = min(sections)
    last_sec = max(sections)
    # Max and Min X/Y Values given random initial values that will be replaced
    # X and Y resolution will be specified by the user in microns (xy_ng_resolution_umx by y_ng_resolution_um)
    max_x = 0
    max_y = 0
    min_x = 9999999
    min_y = 9999999
    # 'min_z' is the relative starting section (if the prep2 sections start at slice 100, and the structure starts at slice 110, min_z is 10 )
    # Z resolution is 20um for simple 1-1 correspondance with section thickness
    max_z = (last_sec)
    min_z = (first_sec)
    # Scaling factor is (0.46/X). Scaling from resolution of 0.46 microns to X microns. x is 10um for neuroglancer in x,y space.
    scale_xy = 0.46 / xy_ng_resolution_um

    # X,Y are 10um voxels. Z is 20um voxels.
    # str_contour_ng_resolution is the previous contour data rescaled
    # to neuroglancer resolution
    str_contour_ng_resolution = {}
    for section, vertices in str_contour.items():
        # Load (X,Y) coordinates on this contour
        #section_contours = str_contour[section][structure]
        # (X,Y) coordinates will be rescaled to the new resolution and placed here
        # str_contour_ng_resolution starts at z=0 for simplicity, must provide section offset later on
        str_contour_ng_resolution[section - first_sec] = []
        # Number of (X,Y) coordinates
        
        num_contours = vertices.shape[0]
        # Cycle through each coordinate pair
        for coordinate_pair in range(num_contours):
            curr_coors = vertices[coordinate_pair]
            # Rescale coordinate pair and add to new contour dictionary
            x = curr_coors[0]
            y = curr_coors[1]
            str_contour_ng_resolution[section - first_sec].append([scale_xy * x, scale_xy * y])
            # Replace Min/Max X/Y values with new extremes
            min_x = min(scale_xy * x, min_x)
            min_y = min(scale_xy * y, min_y)
            max_x = max(scale_xy * x, max_x)
            max_y = max(scale_xy * y, max_y)
    # Cast max and min values to int as they are used to build 3D numpy matrix
    max_x = int(np.ceil(max_x))
    max_y = int(np.ceil(max_y))
    min_x = int(np.floor(min_x))
    min_y = int(np.floor(min_y))

    # Create empty 'structure_volume' using min and max values found earlier. Acts as a bounding box for now
    structure_volume = np.zeros((max_z - min_z, max_y - min_y, max_x - min_x), dtype=np.uint8)
    z_voxels, y_voxels, x_voxels = np.shape(structure_volume)

    # Go through every slice. For every slice color in the voxels corrosponding to the contour's coordinate pair
    for slice in range(z_voxels):
        # For Human Annotated files, sometimes there is a missing set of contours for a slice
        try:
            slice_contour = np.asarray(str_contour_ng_resolution[slice])
        except:
            print('exception creating slice', slice)
            continue

        for xy_pair in slice_contour:
            x_voxel = int(xy_pair[0]) - min_x
            y_voxel = int(xy_pair[1]) - min_y

            structure_volume[slice, y_voxel, x_voxel] = color

            # Instead of coloring a single voxel, color all in a specified radius from this voxel!
            lower_bnd_offset = int(np.floor(1 - color_radius))
            upper_bnd_offset = int(np.ceil(color_radius))
            for x_coor_color_radius in range(lower_bnd_offset, upper_bnd_offset):
                for y_coor_color_radius in range(lower_bnd_offset, upper_bnd_offset):

                    x_displaced_voxel = x_voxel + x_coor_color_radius
                    y_displaced_voxel = y_voxel + y_coor_color_radius
                    distance = ((y_voxel - y_displaced_voxel) ** 2 + (x_voxel - x_displaced_voxel) ** 2) ** 0.5
                    # If the temporary coordinate is within the specified radius AND inside the 3D matrix
                    if distance < color_radius and \
                            x_displaced_voxel < x_voxels and \
                            y_displaced_voxel < y_voxels and \
                            x_displaced_voxel > 0 and \
                            y_displaced_voxel > 0:
                        try:
                            # Set temporary coordinate to be visible
                            structure_volume[slice, y_displaced_voxel, x_displaced_voxel] = color
                        except:
                            print('exception creating structure volume')

    return structure_volume, [min_x, min_y, min_z]



def interpolate(points, new_len):
    pu = points.astype(int)
    indexes = np.unique(pu, axis=0, return_index=True)[1]
    points = np.array([points[index] for index in sorted(indexes)])
    addme = points[0].reshape(1,2)
    points = np.concatenate((points,addme), axis=0)

    tck, u = splprep(points.T, u=None, s=3, per=1) 
    u_new = np.linspace(u.min(), u.max(), new_len)
    x_array, y_array = splev(u_new, tck, der=0)
    return np.concatenate([x_array[:,None],y_array[:,None]], axis=1)



def create_layer(animal, id, start, debug):

    structure_section_vertices = {}
    structure = 'infrahypoglossal'
    template = np.zeros((aligned_shape[1], aligned_shape[0]), dtype=np.uint8)

    with connection.cursor() as cursor:
        sql = """select el.frame + %s as section, el.points 
          from engine_labeledshape el
          inner join engine_job ej on el.job_id = ej.id
          inner join engine_label elab on el.label_id = elab.id
          where elab.task_id = %s
          and elab.name = %s
          order by elab.name, el.frame"""
        cursor.execute(sql, [start, id, structure])
        rows = cursor.fetchall()
    for row in rows:
        section = row[0]
        pts = row[1]
        pts = np.array([tuple(map(float, x.split())) for x in pts.strip().split(',')])
        vertices = pts.reshape(pts.shape[0]//2, 2).astype(np.float64)
        addme = vertices[0].reshape(1,2)
        vertices = np.concatenate((vertices,addme), axis=0)
        lp = vertices.shape[0]
        if lp > 2:
          new_len = max(lp, 100)
          vertices = interpolate(vertices, new_len)

        if debug:
            print(section, vertices.shape, vertices.dtype)
        structure_section_vertices[section] = vertices

    
    volume, xyz_offsets = create_volume(structure_section_vertices, structure, 9)

    print('volume', type(volume), volume.shape, volume.dtype, xyz_offsets)
    ATLAS_DIR = '/net/birdstore/Active_Atlas_Data/data_root/atlas_data'
    outpath = os.path.join(ATLAS_DIR, 'shapes', animal)
    os.makedirs(outpath, exist_ok=True)
    outfile = os.path.join(outpath, f'{structure}.npy')
    np.save(outfile, volume)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on Animal')
    parser.add_argument('--animal', help='Enter animal', required=True)
    parser.add_argument('--id', help='Enter ID', required=True)
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


