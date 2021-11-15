from neuroglancer.models import LayerData
from ajax_datatable.views import AjaxDatatableView
from django.utils.html import format_html


class LayerDataView(AjaxDatatableView):

    model = LayerData
    title = 'Ajax Annotations'
    initial_order = [["animal", "asc"],["layer","asc"],["structure", "asc"], ["user", "asc"],["input_type", "asc"] ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = ' '

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'animal', 'foreign_field': 'prep__prep_id', 'visible': True, 'title':'Animal'},
        {'name': 'layer', 'visible': True, },
        {'name': 'structure', 'foreign_field': 'structure__abbreviation','visible': True, },
        {'name': 'x_f', 'visible': True, 'placeholder':True, 'title': 'X', 'sort_field':'x', 'searchable': False },
        {'name': 'y_f', 'visible': True, 'placeholder':True, 'title': 'Y', 'sort_field':'y', 'searchable': False  },
        {'name': 'z_f', 'visible': True, 'placeholder':True, 'title': 'Section', 'sort_field':'section', 'searchable': False},
        {'name': 'user', 'foreign_field': 'person__username','visible': True, },
        {'name': 'input_type', 'foreign_field': 'input_type__input_type', 'visible': True, },
        {'name': 'updated',  'visible': True, 'searchable': False},
    ]

    def get_initial_queryset(self, request=None):
        # Optimization: Reduce the number of queries due to ManyToMany "tags" relation
        return LayerData.objects.filter(active=True)

    scales = {'dk':0.325, 'md':0.452, 'at':10}

    def customize_row(self, row, obj):
        initial = str(obj.prep_id[0:2]).lower()

        xnumber = int(round(obj.x / self.scales[initial]))
        row['x_f'] = format_html(f"<div style='text-align:left;'>{xnumber:,}</div>")

        ynumber = int(round(obj.y / self.scales[initial]))
        row['y_f'] = format_html(f"<div style='text-align:left;'>{ynumber:,}</div>")

        znumber = int(round(obj.section / 20))
        row['z_f'] = format_html(f"<div style='text-align:left;'>{znumber:,}</div>")
        return

