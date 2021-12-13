from django.db import models
import json
from django.conf import settings
from django.contrib import admin
from django.forms import TextInput
from django.utils.html import format_html, escape

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer
from django.utils.safestring import mark_safe
from brain.admin import AtlasAdminModel, ExportCsvMixin
from neuroglancer.models import InputType, LayerData, \
    NeuroglancerModel,  Structure
from neuroglancer.forms import NeuroglancerModelForm, NeuroglancerUpdateForm

def datetime_format(dtime):
    return dtime.strftime("%d %b %Y %H:%M")

@admin.register(NeuroglancerModel)
class NeuroglancerModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }
    list_display = ('animal', 'open_neuroglancer', 'lab',
                    'person', 'updated')
    ordering = ['-updated']
    # exclude = ['neuroglancer_state']
    list_filter = ['updated', 'created']
    search_fields = ['comments']

    def add_view(self, request, extra_content=None):
        """Add a new state object with just the title and drop down of animals"""
        self.exclude = ('animal','states', 'pretty_url', 'created', 'user_date', 'updated')
        self.readonly_fields = []
        self.change_form_template = "create_state.html"    
        return super(NeuroglancerModelAdmin, self).add_view(request)

    def change_view(self, request, object_id, extra_content=None):
        """View existing state with most of the fields excluded or readonly"""
        self.exclude = ('neuroglancer_state', 'user_date', 'panels', 'animal')
        self.readonly_fields = ['pretty_url', 'created', 'updated']
        return super(NeuroglancerModelAdmin, self).change_view(request, object_id)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not change:
            print('save model not change')
            self.form.prepareModel(self, request, obj, form, change)
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, change=None, **kwargs):
        """
        Use special form only for adding. For viewing, create a pretty json
        format and only allow the title to be changed.
        """
        if not obj:
            self.form = NeuroglancerModelForm
        else:
            #form = super().get_form(request, obj=obj, change=change, **kwargs)
            self.form = NeuroglancerUpdateForm
        return self.form

    def get_queryset(self, request, obj=None):
        user = request.user
        rows = None
        if user.labs is not None and not user.is_superuser:
            lab_ids = [p.id for p in user.labs.all()]
            rows = NeuroglancerModel.objects.filter(person__lab__in=lab_ids).order_by('-updated')
        else:
            rows = NeuroglancerModel.objects.order_by('-updated')
            
        return rows


    def pretty_url(self, instance):
        """Function to display pretty version of our data"""

        # Convert the data to sorted, indented JSON
        response = json.dumps(instance.neuroglancer_state, sort_keys=True, indent=2)
        # Truncate the data. Alter as needed
        # response = response[:5000]
        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')
        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)
        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        # Safe the output
        return mark_safe(style + response)

    pretty_url.short_description = 'Formatted URL'

    def open_neuroglancer(self, obj):
        host = "https://activebrainatlas.ucsd.edu/ng"
        if settings.DEBUG:
            host = "http://127.0.0.1:8080"

        comments = escape(obj.comments)
        links = f'<a target="_blank" href="{host}?id={obj.id}">{comments}</a>'
        return format_html(links)

    def open_multiuser(self, obj):
        host = "https://activebrainatlas.ucsd.edu/ng_multi"
        if settings.DEBUG:
            host = "http://127.0.0.1:8080"

        comments = "Testing"
        links = f'<a target="_blank" href="{host}?id={obj.id}&amp;multi=1">{comments}</a>'
        return format_html(links)
    
    def lab(self, obj):
        lab = "NA"
        if obj.person is not None and obj.person.lab is not None:
            lab = obj.person.lab
        return lab

    open_neuroglancer.short_description = 'Neuroglancer'
    open_neuroglancer.allow_tags = True
    open_multiuser.short_description = 'Multi-User'
    open_multiuser.allow_tags = True
    lab.short_description = "Lab"

@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('abbreviation', 'description','active','created_display')
    ordering = ['abbreviation']
    readonly_fields = ['created']
    list_filter = ['created', 'active']
    #list_filter = (VettedFilter,)
    search_fields = ['abbreviation', 'description']

    def created_display(self, obj):
        return datetime_format(obj.created)
    created_display.short_description = 'Created'    

    def show_hexadecimal(self, obj):
        return format_html('<div style="background:{}">{}</div>',obj.hexadecimal,obj.hexadecimal)

    show_hexadecimal.short_description = 'Hexadecimal'

def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
make_inactive.short_description = "Mark selected COMs as inactive"

def make_active(modeladmin, request, queryset):
    queryset.update(active=True)
make_active.short_description = "Mark selected COMs as active"

@admin.register(InputType)
class InputTypeAdmin(AtlasAdminModel):
    list_display = ('id', 'input_type', 'description', 'active','created')
    ordering = ['id']
    readonly_fields = ['created', 'updated']
    list_filter = ['created', 'active']
    search_fields = ['input_type', 'description']

@admin.register(LayerData)
class LayerDataAdmin(AtlasAdminModel):
    # change_list_template = 'layer_data_group.html'
    list_display = ('prep_id', 'structure', 'layer', 'person', 'x_f', 'y_f', 'z_f', 'active')
    ordering = ['prep', 'layer','structure__abbreviation', 'section']
    excluded_fields = ['created', 'updated']
    list_filter = ['created', 'active','input_type']
    search_fields = ['prep__prep_id', 'structure__abbreviation', 'layer', 'person__username']
    scales = {'dk':0.325, 'md':0.452, 'at':10}

    def get_queryset(self, request, obj=None):
        user = request.user
        rows = None
        if user.lab is not None:
            rows = LayerData.objects.filter(person__lab=user.lab)\
            .order_by('prep', 'layer','structure__abbreviation', 'section')
        else:
            rows = LayerData.objects.order_by('prep', 'layer','structure__abbreviation', 'section')
            
        return rows

    def save_model(self, request, obj, form, change):
        obj.person = request.user
        super().save_model(request, obj, form, change)

    def x_f(self, obj):
        initial = str(obj.prep_id[0:2]).lower()
        number = int(round(obj.x / self.scales[initial]))
        return format_html(f"<div style='text-align:left;'>{number:,}</div>")
    def y_f(self, obj):
        initial = str(obj.prep_id[0:2]).lower()
        number = int(round(obj.y / self.scales[initial]))
        return format_html(f"<div style='text-align:left;'>{number:,}</div>")
    def z_f(self, obj):
        number = int(obj.section / 20)
        return format_html(f"<div style='text-align:left;'>{number:,}</div>")

    x_f.short_description = "X"
    y_f.short_description = "Y"
    z_f.short_description = "Section"
