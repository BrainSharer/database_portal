from authentication.models import User


def user_get_me(*, user: User):
    print('userxxxxxxxxxxxxxxxxxxxxxxxxx', user)
    return {
        'id': user.id,
        'name': user.first_name,
        'email': user.email
    }


def jwt_response_payload_handler(user, token=None, request=None):
    print('xxxxxxxxxxxxxxxxx', token)
    return {
        'token': 'token here',
        'me': user_get_me(user=user),
    }