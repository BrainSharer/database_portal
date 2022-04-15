import os, sys
import argparse

HOME = os.path.expanduser("~")
PATH = os.path.join(HOME, 'programming/brainsharer_portal')
sys.path.append(PATH)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brainsharer.settings")
import django
django.setup()

from brain.models import Animal

def fetch_animals(debug):
    data = []
    animals = Animal.objects.filter(active=1)
    for animal in animals:
        data.append(animal.animal_name)
        if debug:
            print(animal.animal_name)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work on Animal')
    parser.add_argument('--debug', help='Enter debug True|False', required=False, default='false')

    args = parser.parse_args()
    debug = bool({'true': True, 'false': False}[str(args.debug).lower()])
    fetch_animals(debug)




                
        


