from django.urls import include, path
from brain import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'animal', views.Animal, basename='animal')


urlpatterns = [
    path('', include(router.urls)),
    # path('animal/<str:pk>', views.AnimalDetail.as_view()),
]