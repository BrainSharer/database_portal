from django.urls import path
from brain import views

urlpatterns = [
    path(r'image-listing', views.image_list),
    path('animals', views.AnimalList.as_view()),
    path('animal/<str:pk>', views.AnimalDetail.as_view()),
]