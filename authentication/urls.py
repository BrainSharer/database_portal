from django.urls import include, path
from rest_framework import routers
from authentication.views import SessionVarView, dev_login_view, RegisterView

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'session', SessionVarView.as_view(), name='session-var'),
    path(r'devlogin/', dev_login_view, name='devlogin'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
