from django.urls import path

from authentication.views import SessionVarView, dev_login_view

urlpatterns = [
    path(r'session', SessionVarView.as_view(), name='session-var'),
    path(r'devlogin/', dev_login_view, name='devlogin'),
]
