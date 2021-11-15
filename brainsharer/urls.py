from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from brainsharer.views import SessionVarView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'session', SessionVarView.as_view(), name='session-var'),
    path('', include('brain.urls')),
    path('', include('neuroglancer.urls')),
]

urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    pass
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

