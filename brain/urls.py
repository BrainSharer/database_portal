from django.urls import path
from brain import views

urlpatterns = [
    path('animals', views.AnimalList.as_view()),
    path('animal/<str:pk>', views.AnimalDetail.as_view()),
]