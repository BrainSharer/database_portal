'''
WE need to import the settings.DEBUG here as when developing on a local machine,
the urls don't have the brainsharer in them
'''
from django.urls import path, include
from neuroglancer import views
from neuroglancer.create_state_views import fetch_layers
from rest_framework import routers
from django.conf import settings
app_name = 'neuroglancer'

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'neuroglancer', views.NeuroglancerViewSet, basename='neuroglancer')
router.register(r'states', views.NeuroglancerAvailableData, basename='states')

urlpatterns = [
    path('', include(router.urls)),
    path(r'public', views.public_list, name='public'),
    path('annotation/<int:animal_id>/<str:label>', views.Annotation.as_view()),
    path('annotations', views.Annotations.as_view()),
    path('groups', views.NeuroglancerGroupAvailableData.as_view()),
    path('landmark_list',views.LandmarkList.as_view()),
    path('createstate', views.create_state),
    path('fetch_layers/<int:animal_id>', fetch_layers, name='fetch_layers'),
    path('mlneurons/<str:atlas_name>/<str:neuron_parts_boolstr>/soma/<str:brain_region1>',
        views.MouseLightNeuron.as_view()),

    path('mlneurons/<str:atlas_name>/<str:neuron_parts_boolstr>/soma/<str:brain_region1>/soma/<str:brain_region2>',
        views.MouseLightNeuron.as_view()),
    path('mlneurons/<str:atlas_name>/<str:neuron_parts_boolstr>/<str:filter_type1>/<str:brain_region1>/<str:operator_type1>/<int:thresh1>',
        views.MouseLightNeuron.as_view()),

    path('mlneurons/<str:atlas_name>/<str:neuron_parts_boolstr>/<str:filter_type1>/<str:brain_region1>/<str:operator_type1>/<int:thresh1>/soma/<str:brain_region2>',
        views.MouseLightNeuron.as_view()),

    path('mlneurons/<str:atlas_name>/<str:neuron_parts_boolstr>/soma/<str:brain_region1>/<str:filter_type2>/<str:brain_region2>/<str:operator_type2>/<int:thresh2>',
        views.MouseLightNeuron.as_view(),name='test'),

    path('mlneurons/<str:atlas_name>/<str:neuron_parts_boolstr>/<str:filter_type1>/<str:brain_region1>/<str:operator_type1>/<int:thresh1>/<str:filter_type2>/<str:brain_region2>/<str:operator_type2>/<int:thresh2>',
        views.MouseLightNeuron.as_view()),

    path('anatomical_regions/<str:atlas_name>',views.AnatomicalRegions.as_view()),

    path('tracing_annotations/<str:virus_timepoint>/<str:primary_inj_site>',
        views.TracingAnnotation.as_view()),
]


if settings.DEBUG:
    urlpatterns += path('brainsharer/fetch_layers/<int:animal_id>', fetch_layers, name='fetch_layers'),
