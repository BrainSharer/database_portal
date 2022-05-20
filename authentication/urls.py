from django.urls import include, path
from rest_framework import routers
from authentication import views 
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView


router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'labs', views.LabViewSet, basename='labs')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'session', views.SessionVarView.as_view(), name='session-var'),
    path(r'devlogin/', views.dev_login_view, name='devlogin'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('validate/', views.ValidateUserView.as_view(), name='auth_validate'),
    path('user/<str:username>', views.UserView.as_view(), name='fetch_user'),
    path(r'login', views.ObtainJWTView.as_view()),
    path(r'api/v1/api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/v1/api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
