from django.urls import include, path
from rest_framework import routers
from authentication.views import SessionVarView, dev_login_view, \
    RegisterView, UserView, ValidateUserView, ObtainJWTView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'session', SessionVarView.as_view(), name='session-var'),
    path(r'devlogin/', dev_login_view, name='devlogin'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('validate/', ValidateUserView.as_view(), name='auth_validate'),
    path('user/<str:username>', UserView.as_view(), name='fetch_user'),
    path(r'login', ObtainJWTView.as_view()),
    path(r'api/v1/api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/v1/api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
