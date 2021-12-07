from django.urls import path, include
from neuroglancer import views
from neuroglancer.create_state_views import fetch_layers
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
    path('fetch_layers/<str:animal>', fetch_layers, name='fetch_layers')
]