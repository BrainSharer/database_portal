import json
from django.shortcuts import render
from django.http import HttpResponse
from celery import chain
from celery.result import AsyncResult
from workflow.tasks import setup, make_meta, make_tifs, make_scenes

def progress_view(request):
    animal = 'DK54'
    channel = 1
    njobs = 2

    result = chain(
        setup.si(animal),
        make_meta.si(animal),
        make_tifs.si(animal, channel, njobs),
        make_scenes.si(animal, njobs)
    ).apply_async()
    scene_id =  result.id
    meta_id = result.parent.id
    tif_id =  result.parent.parent.id
    setup_id = result.parent.parent.parent.id
    
    celery_task_ids = {}
    for i, task_id in enumerate([setup_id, tif_id, meta_id, scene_id]):
        celery_task_ids[i] = task_id
    
    return render(request, 'pipeline.html', context={'celery_task_ids': celery_task_ids})

def progress_test(request):
    animal = 'DK54'
    channel = 1
    njobs = 2
    
    return render(request, 'pipeline.html', context={'animal': animal, 'opts': ''})


def get_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


