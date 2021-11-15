from neuroglancer.models import LayerData
from datetime import datetime
import numpy as np
from brain.models import Animal
from neuroglancer.models import Structure
from django.contrib.auth.models import User

animal = 'DK39'
prep = Animal.objects.get(pk=animal)
structure = 'point'
layer ='detected_soma'
SURE = 6
UNSURE = 7
structure = Structure.objects.get(abbreviation=structure)
loggedInUser = User.objects.get(pk=26)
for i in range (10):
    x,y,z = np.random.rand(3)*10000
    LayerData.objects.create(
        prep=prep, structure=structure, created=datetime.now(),
        layer = layer, active=True, person=loggedInUser, input_type_id=SURE,
        x=x, y=y, section=z)

    x,y,z = np.random.rand(3)*10000
    LayerData.objects.create(
        prep=prep, structure=structure, created=datetime.now(),
        layer = layer, active=True, person=loggedInUser, input_type_id=UNSURE,
        x=x, y=y, section=z)