from django.urls import include, path
from rest_framework import routers
from authentication import views 
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import refresh_jwt_token
from authentication.apis import GoogleLoginApi, LoginApi
app_name = 'authentication'

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'labs', views.LabViewSet, basename='labs')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('session', views.SessionVarView.as_view(), name='session-var'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('validate/', views.ValidateUserView.as_view(), name='auth_validate'),
    path('user/<str:username>', views.UserView.as_view(), name='fetch_user'),
    path('api-token-auth/', obtain_auth_token, name='obtain-token'),
    path('api-token-refresh/', refresh_jwt_token, name='refresh-token'),
    path('api-token-login/', LoginApi.as_view(), name='login'),
    path('google/', GoogleLoginApi.as_view(), name='login-with-google'),
    path('hello/', views.HelloView.as_view(), name='hello'),    
]
