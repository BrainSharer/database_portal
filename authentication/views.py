from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User
from django.conf import settings

from rest_framework import generics
from rest_framework import permissions
from authentication.serializers import RegisterSerializer, ValidateUserSerializer

class SessionVarView(TemplateView):
    '''
    This gets the session var from Neuroglancer to check
    if the user is logged in. Note, this works fine on the
    production server, but since Neuroglancer and Django
    run on different ports locally, it is a pain to translate
    between the two. To test Neuroglancer locally:
        for login, comment out the if statement,
        when you do this, the user will ALWAYS appear to be not logged in! This
        is because of the different ports!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''

    def get(self, request, *args, **kwargs):
        data = {'user_id':0, 'username': None}
        if request.user.is_authenticated:
            data = {'user_id':request.user.id, 'username': request.user.username}
        
        if settings.DEBUG and False:
            userid = 1
            browser = str(request.META['HTTP_USER_AGENT']).lower()
            if 'firefox' in browser:
                userid = 2
            user = User.objects.get(pk=userid) 
            data = {'user_id':user.id, 'username': user.username}
        
        return JsonResponse(data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ValidateUserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ValidateUserSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            return queryset.filter(username=username)

        email = self.request.query_params.get('email')
        if email is not None:
            return queryset.filter(email=email)

        return User.objects.filter(pk=0)


@login_required(redirect_field_name='next', login_url='/devlogin')
def dev_login_view(request):
    '''
    This is only used when the developer is working locally. This is called
    from services/service.ts in neuroglancer as: http://localhost:8000/admin/login/?next=/devlogin/?id=2
    This method turns everything after the 'next' into http://localhost:8080/?id=2 
    That is the local neuroglancer url. None of this is necessary when you are
    on the production server
    :param request: incoming request after the user logs in
    '''
    nid = request.GET.get("id", None)
    if nid is None:
        return redirect("http://localhost:8000/admin")
    else:
        return redirect(f"http://localhost:8080/?id={nid}")
