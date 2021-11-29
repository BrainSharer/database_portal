from django.urls import path, include
from neuroglancer import views
#from neuroglancer import ajax_datatable_views
from rest_framework import routers
app_name = 'neuroglancer'

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'neuroglancer', views.NeuroglancerViewSet, basename='neuroglancer')

urlpatterns = [
    path('', include(router.urls)),
    path(r'public', views.public_list, name='public'),
    path('annotation/<str:prep_id>/<str:layer_name>/<int:input_type_id>', views.Annotation.as_view()),
    path('annotations', views.Annotations.as_view()),
    path('landmark_list',views.LandmarkList.as_view()),
    path('mlneurons/<str:atlas_name>/<str:brain_region>/<str:filter_type>/<str:operator_type>/<int:thresh>',
        views.MouseLightNeuron.as_view()),
    path('anatomical_regions/<str:atlas_name>',views.AnatomicalRegions.as_view())
]