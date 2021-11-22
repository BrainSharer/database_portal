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
from pickle import NONE
def datetime_format(dtime):
    return dtime.strftime("%d %b %Y %H:%M")

@admin.register(NeuroglancerModel)
class NeuroglancerModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
    }
    list_display = ('animal', 'open_neuroglancer', 'open_multiuser',
                    'person', 'updated')
    ordering = ['-vetted', '-updated']
    readonly_fields = ['pretty_url', 'created', 'user_date', 'updated']
    exclude = ['neuroglancer_state']
    list_filter = ['updated', 'created', 'vetted']
    search_fields = ['comments']

    def get_queryset(self, request, obj=None):
        user = request.user
        rows = None
        if user.lab is not None:
            rows = NeuroglancerModel.objects.filter(person__lab=user.lab).order_by('updated').all()
        else:
            rows = NeuroglancerModel.objects.order_by('updated').all()
            
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

    open_neuroglancer.short_description = 'Neuroglancer'
    open_neuroglancer.allow_tags = True
    open_multiuser.short_description = 'Multi-User'
    open_multiuser.allow_tags = True

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
