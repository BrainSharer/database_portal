from django.conf.urls import url
from django.urls import path
from workflow.views import get_progress
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='tasks.html')),
    path('<int:task_id>', get_progress, name='task_status'),
]
