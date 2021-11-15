from django.contrib import admin
from django.forms import TextInput, Textarea, DateInput, NumberInput, Select
from django.db import models
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count
from django.utils.html import strip_tags
from plotly.offline import plot
import plotly.graph_objects as go

from neuroglancer.models import UrlModel
from brain.models import Animal
from workflow.models import Task, ProgressLookup, TaskView, Log, Journal, \
    Problem, FileLog, TableMetadata

from workflow.forms import PipelineForm
from celery import chain
from workflow.tasks import setup, make_meta, make_tifs, make_scenes


class WorkflowAdminModel(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.DateTimeField: {'widget': DateInput(attrs={'size':'20'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':100})},
    }

@admin.register(ProgressLookup)
class ProgressLookupAdmin(admin.ModelAdmin):
    list_display = ('description', 'script', 'action', 'channel', 'downsample')
    search_fields = ('description',)
    ordering = ['description']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('prep_id', 'task', 'is_complete')
    search_fields = ('prep__prep_id',)
    ordering = ['prep', 'lookup']
    list_filter = ['created']

    def is_complete(self, instance):
        return instance.completed == 1

    is_complete.boolean = True

    def task(self, instance):
        return instance.lookup.description

    def prep_id(self, instance):
        return instance.prep.prep_id

    def view_pipeline(self, request):
        celery_task_ids = {}
        animal = None
        title = 'Active Brain Atlas Pipeline'
        
        if request.method == 'POST':
            form = PipelineForm(request.POST)


            if form.is_valid():
                animal = form.cleaned_data['animal']
                print(f'type of animal is {type(animal)}')
                # do celery stuff here.
                animal = animal.prep_id
                
                result = chain(
                    setup.si(animal),
                    make_meta.si(animal),
                    make_tifs.si(animal, 1, 3),
                    make_scenes.si(animal, 3)
                ).apply_async()
                scene_id =  result.id
                meta_id = result.parent.id
                tif_id =  result.parent.parent.id
                setup_id = result.parent.parent.parent.id                
                ids = [setup_id, tif_id, meta_id, scene_id]
                
                #result = setup.delay(animal)
                #ids = [result.id]
                print(result.status, ids)
                for i, task_id in enumerate(ids):
                    celery_task_ids[i] = task_id
                celery_task_ids = celery_task_ids
                title = f'Active Brain Atlas {animal} Pipeline'
                form = None

        else:
            form = PipelineForm()
        

        context = dict(
            self.admin_site.each_context(request),
            title = title,
            form = form,
            animal = animal,
            celery_task_ids = celery_task_ids
        )
        return TemplateResponse(request, "pipeline.html", context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('pipeline/', self.admin_site.admin_view(self.view_pipeline))
        ]
        return my_urls + urls
       

@admin.register(TaskView)
class TaskViewAdmin(admin.ModelAdmin):
    list_display = ('prep_id', 'percent_complete')
    change_list_template = "admin/task_view.html"
    ordering = ['prep_id']
    readonly_fields = ['prep_id', 'percent_complete']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(TaskViewAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    def changelist_view(self, request, extra_context=None):
        counts = Task.objects.all().filter(lookup__channel__in=[0,1]).filter(lookup__downsample=False)\
        .filter(prep__active=True)\
        .values('prep_id').annotate(total=Count('prep_id')).order_by('prep_id')
        animals = Animal.objects.filter(active=True).order_by('prep_id').all()
        lookups = ProgressLookup.objects.filter(channel__in=[0,1]).filter(downsample=False).order_by('id').all()

        al = []
        x = [] 
        i = 0
        for animal in animals:
            if animal.aliases_1 is None:
                continue
            al.append(str(animal.prep_id + '-' + animal.aliases_1))
            x.append(counts[i]['total'])
            i += 1

        lookup_list = []
        id_list = []
        for i, lookup in enumerate(lookups):
            id_list.append(i)
            lookup_list.append(lookup.action)
        limit = len(lookup_list)
        colors = [x*19 for x in range(len(x))]
        marker={'color': colors, 'colorscale': 'Viridis'}
        fig = go.Figure(data=[go.Bar(x=x, y=al, orientation='h', marker=marker )])
        fig.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, height=600)
        fig.update_xaxes(ticks='outside',tickwidth=2, tickangle=45, tickcolor='crimson', ticklen=10, range=[0,limit-1])
        fig.update_layout(autosize=True, xaxis=dict(tickmode='array', tickvals=id_list, ticktext=lookup_list),
                  margin=dict(l=20, r=20, t=20, b=280),
                  paper_bgcolor="LightSteelBlue",
                  )                                  
        gantt_div = plot(fig, output_type='div', include_plotlyjs=False)
        # Serialize and attach the workflow data to the template context
        extra_context = extra_context or {"gantt_div": gantt_div, 'title':'Pipeline Progress by Animal'}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)



@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('prep_id', 'level', 'logger', 'msg', 'created')
    ordering = ['prep_id', 'created']
    list_filter = ['created', 'level']
    list_display_links = None
    search_fields = ['prep__prep_id', 'msg']


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Journal)
class JournalAdmin(WorkflowAdminModel):
    list_display = ('prep_id', 'issue_tag', 'person', 'problem', 'completed', 'link_tag', 'created')
    ordering = ['prep_id', 'created']
    list_filter = ['created', 'completed']
    search_fields = ['prep__prep_id','entry']
    fields = ['prep', 'url', 'section','channel', 'entry', 'fix', 'person', 'problem', 'completed', 'active', 'image','issue_link', 'image_tag']
    readonly_fields = ['image_tag', 'link_tag', 'issue_tag']

    def prep_id(self, instance):
        return instance.prep.prep_id

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["widget"] = Select(attrs={'style': 'width: 250px;'})
        if db_field.name == "url":
            kwargs["queryset"] = UrlModel.objects.order_by('comments')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('problem_category', 'active', 'created')


@admin.register(TableMetadata)
class TableMetadataAdmin(admin.ModelAdmin):
    list_display = ('tablename', 'category', 'created')
    readonly_fields = ['pretty_entry']
    exclude = ['entry'] 
    list_filter = ['category']

    def pretty_entry(self, obj):
        return strip_tags(obj.entry)

    pretty_entry.short_description = 'Formatted Metadata'
    

    def has_add_permission(self, request):
        return False


@admin.register(FileLog)
class FileLogAdmin(admin.ModelAdmin):
    list_display = ('prep_id', 'filename')
