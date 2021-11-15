# How Neuroglancer Aligns a Brain to the Atlas
1. All python code is located within the Django REST code which is this repository. 
1. There are several files in this repository which are used for this process:
    1. [views.py](views.py)
    1. [atlas.py](atlas.py)
1. In Neuroglancer the user selects a brain from a dropdown menu which has 3 variables to send to the REST API.
    1. Brain ID
    1. Input type (currently we are only using the 'corrected' COMs)
    1. User ID (currently this defaults to Beth as she did all the manual entry of the COMs)
1. Neuroglancer makes a REST call via this url:  https://activebrainatlas.ucsd.edu/activebrainatlas/rotation/DK39/corrected/2
1. In the url above, DK39 is the Brain ID, 'corrected' is the input type and 2 is Beth's ID.
1. That url then calls the `get` method in the `Rotation` class in this file: [views.py](views.py)
1. That method calls the `align_atlas` method in the [atlas.py](atlas.py) and returns the JSON to Neuroglanccer.
1. The `align_atlas` method fetches the appropriate data from the Atlas COMs and the brain's COM's. That data is then used to create the rotation and translation matrices by using `align_point_sets` method.