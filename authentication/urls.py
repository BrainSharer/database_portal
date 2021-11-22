from django.urls import path

from authentication.views import SessionVarView

urlpatterns = [
    path(r'session', SessionVarView.as_view(), name='session-var'),
]
