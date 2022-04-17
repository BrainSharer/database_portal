from django.contrib import admin
from django.forms import TextInput, Textarea, DateInput, NumberInput, Select
from django.db import models
import csv
from django.http import HttpResponse
from django.contrib.admin.widgets import AdminDateWidget
from django.urls import path
from django.template.response import TemplateResponse

from brain.models import Animal, Biocyc, Injection, Virus, InjectionVirus, \
    ScanRun, BrainRegion, BrainAtlas


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        excludes = ['histogram',  'image_tag']
        field_names = [field.name for field in meta.fields if field.name not in excludes]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class AtlasAdminModel(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Select(attrs={'size':'250'})},
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.DateTimeField: {'widget': DateInput(attrs={'size':'20'})},
        # models.DateField: {'widget': DateTimeInput(attrs={'size':'20','type':'date'})},
        models.DateField: {'widget': AdminDateWidget(attrs={'size':'20'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    def is_active(self, instance):
        return instance.active == 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["widget"] = Select(attrs={
            'style': 'width: 250px;'
        })
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    is_active.boolean = True

    list_filter = ('created', )
    fields = []
    actions = ["export_as_csv"]

    class Media:
        css = {
            'all': ('admin/css/thumbnail.css',)
        }

@admin.register(Biocyc)
class BiocycAdmin(AtlasAdminModel, ExportCsvMixin):
    list_display = ('bio_name', 'created')
    search_fields = ('bio_name',)
    ordering = ['bio_name']


@admin.register(Animal)
class AnimalAdmin(AtlasAdminModel, ExportCsvMixin):
    list_display = ('animal_name', 'lab', 'comments', 'created')
    search_fields = ('animal_name',)
    ordering = ['animal_name']
    exclude = ('created',)

    def view_pipeline(self, request):
        context = dict(
            self.admin_site.each_context(request),
            title="sdfsdfsdf"
        )
        return TemplateResponse(request, "basic.html", context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('pipeline/', self.admin_site.admin_view(self.view_pipeline))
        ]
        return my_urls + urls

@admin.register(Injection)
class InjectionAdmin(AtlasAdminModel, ExportCsvMixin):
    list_display = ('animal', 'performance_center', 'anesthesia', 'comments', 'created')
    search_fields = ('animal__animal',)
    ordering = ['created']

@admin.register(Virus)
class VirusAdmin(AtlasAdminModel, ExportCsvMixin):
    list_display = ('virus_name', 'virus_type', 'type_details', 'created')
    search_fields = ('virus_name',)
    ordering = ['virus_name']

@admin.register(InjectionVirus)
class InjectionVirusAdmin(AtlasAdminModel):
    list_display = ('animal', 'injection_comments', 'virus_name', 'created')
    fields = ['injection', 'virus']
    search_fields = ('injection__animal__animal',)
    ordering = ['created']

    def animal(self, instance):
        return instance.injection.animal.animal
    
    def injection_comments(self, instance):
        return instance.injection.comments

    def virus_name(self, instance):
        return instance.virus.virus_name

@admin.register(ScanRun)
class ScanRunAdmin(AtlasAdminModel, ExportCsvMixin):
    list_display = ('animal', 'resolution', 'zresolution', 'created')
    search_fields = ('animal__animal_name',)
    ordering = ['animal', 'comments', 'created']
    
@admin.register(BrainRegion)
class BrainRegionAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('abbreviation', 'description','active','created')
    ordering = ['abbreviation']
    readonly_fields = ['created']
    list_filter = ['created', 'active']
    search_fields = ['abbreviation', 'description']
    
@admin.register(BrainAtlas)
class BrainAtlasAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('atlas_name', 'description','active','created')
    ordering = ['atlas_name', 'active']
    readonly_fields = ['created']
    list_filter = ['created', 'active']
    search_fields = ['abbreviation', 'description']


@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = ['action_time', 'action_flag']
    search_fields = ['object_repr', 'change_message']
    list_display = ['action_time', 'user', 'content_type', 'action_flag']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.site_header = 'BrainSharer Admin'
admin.site.site_title = "BrainSharer"
admin.site.index_title = "Welcome to Brainsharer Portal"
admin.site.site_url = "https://www.brainsharer.org"
