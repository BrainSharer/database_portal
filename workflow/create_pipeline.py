#from celery import chain
from celery.result import AsyncResult
from workflow.tasks import setup, make_meta, make_tifs, make_scenes

if __name__ == '__main__':
    animal = 'DK55555'
    channel = 1
    njobs = 3

    worker = setup.delay(animal)

    print(worker.status)
