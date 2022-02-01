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

urlpatterns = [
    path('', include(router.urls)),
    path(r'public', views.public_list, name='public'),
    path('annotation/<int:animal_id>/<str:label>/<int:FK_input_id>', views.Annotation.as_view()),
    path('annotations', views.Annotations.as_view()),
    path('landmark_list',views.LandmarkList.as_view()),
    path('fetch_layers/<int:animal_id>', fetch_layers, name='fetch_layers')
]

if settings.DEBUG:
    urlpatterns += path('brainsharer/fetch_layers/<int:animal_id>', fetch_layers, name='fetch_layers'),
