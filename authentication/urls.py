from django.urls import include, path
from rest_framework import routers
from authentication import views 
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from authentication.apis import GithubLoginApi, GoogleLoginApi
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
    path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('github/', GithubLoginApi.as_view(), name='login-with-github'),
    path('google/', GoogleLoginApi.as_view(), name='login-with-google'),
]
