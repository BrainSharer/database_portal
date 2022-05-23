from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.utils import get_username_field
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, user_logged_in
from django.utils.translation import ugettext_lazy as _

from authentication.models import Lab, User
from authentication.utils import unix_epoch


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'



class ValidateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        try:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
        except ValidationError as ex:
            print('do we get ehre')
            raise serializers.ValidationError(f'error {ex}')    

        user.set_password(validated_data['password'])
        user.save()

        return user


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            # msg = msg.format()
            raise serializers.ValidationError(msg)


class JSONWebTokenSerializer(serializers.Serializer):
    """
    Serializer class used to validate a username and password.
    'username' is identified by the custom UserModel.USERNAME_FIELD.
    Returns a JSON Web Token that can be used to authenticate later calls.
    """

    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        """Dynamically add the USERNAME_FIELD to self.fields."""
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field
                    ] = serializers.CharField(write_only=True, required=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, data):
        credentials = {
            self.username_field: data.get(self.username_field),
            'password': data.get('password')
        }

        user = authenticate(self.context['request'], **credentials)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)

        payload = JSONWebTokenAuthentication.jwt_create_payload(user)

        return {
            'token': JSONWebTokenAuthentication.jwt_encode_payload(payload),
            'user': user,
            'issued_at': payload.get('iat', unix_epoch())
        }