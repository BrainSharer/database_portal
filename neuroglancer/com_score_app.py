from neuroglancer.AlignmentScore import AlignmentScore
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

alignmentPlot = DjangoDash('AlignmentPlot',
                           external_stylesheets=external_stylesheets)

alignmentPlot.layout = html.Div(children=[
    dcc.Graph(id='plot'),
    html.Label('Select plot type'),
    dcc.RadioItems(id='plottype',
            options=[
                {'label': 'scatter plot', 'value': 'scatter'},
                {'label': u'box plot', 'value': 'box_plot'},
            ],
        value='scatter'
    ),
])


@alignmentPlot.expanded_callback(
    Output('plot', 'figure'),
    [Input('plottype', 'value')])
def update_figure(figure_type):
    align_score = AlignmentScore()
    fig = align_score.get(figure_type)
    return fig
