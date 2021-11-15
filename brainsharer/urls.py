"""activebrainatlas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from activebrainatlas.views import SessionVarView
from workflow.gantt_view import gantt

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'graph', gantt),
    path(r'gantt', TemplateView.as_view(template_name='gantt.html')),
    path(r'session', SessionVarView.as_view(), name='session-var'),
    # path(r'urldata', UrlDataView.as_view(), name='get-data'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', include('brain.urls')),
    path('', include('neuroglancer.urls')),
    path('', include('workflow.urls')),
    re_path(r'^celery-progress/', include('celery_progress.urls')), 
]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

