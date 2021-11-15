from django.shortcuts import render
from plotly.offline import plot
import plotly.figure_factory as ff

from brain.models import Animal
from brain.forms import AnimalForm
from workflow.models import Task



def gantt(request):
    # from url initial page
    prep_id = request.GET.get('prep_id')
    if not prep_id:
        prep_id = 'DK43'

    form = AnimalForm()  # A form bound to the GET data
    animals = Animal.objects.filter(prep_id=prep_id).order_by('prep_id')
    animal = Animal.objects.get(prep_id=prep_id)
    tasks = Task.objects.all()

    df  = []
    for entry in tasks:
        task = dict(Task=entry.name, Start=entry.start_date, Finish=entry.end_date)
        df.append(task)
    fig = ff.create_gantt(df)
    gantt_div = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'tasks.html', context={'animals': animals,
                                                  'animal': animal,
                                                  'form': form,
                                                  'gantt_div': gantt_div,
                                                  'animal_title': prep_id})
