import json
import jwt
import requests

from django.apps import apps
from django.conf import settings
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header
)

def get_user_model():
    return apps.get_model(settings.API_AUTH_USER_MODEL, require_ready=False)

def get_cognito_endpoint():
    region = settings.COGNITO_AWS_REGION
    userpool = settings.COGNITO_USER_POOL
    return f'https://cognito-idp.{region}.amazonaws.com/{userpool}/'


class CognitoAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or smart_text(auth[0].lower()) != 'bearer':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                'Invalid basic header.'
                'Credentials string should not contain spaces.'
            )
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, jwt_token):
        try:
            jwt_response = requests.get(
                f'{get_cognito_endpoint()}.well-known/jwks.json'
            )
            jwt_response.raise_for_status()
            jwt_json_data = jwt_response.json()
            jwt_public_key = jwt.algorithms.RSAAlgorithm.from_jwk({
                item['kid']: json.dumps(item) for item in jwt_json_data['keys']
            })
            jwt_data = jwt.decode(
                token=jwt_token,
                public_key=jwt_public_key,
                audience=settings.COGNITO_AUDIENCE,
                issuer=get_cognito_endpoint(),
                algorithms=['RS256'],
            )
        except:
            msg = _('Invalid authorization header.')
            raise exceptions.AuthenticationFailed(msg)

        print(jwt_data)
        user, _ = get_user_model().objects.get_or_create(
            cognito_id=jwt_data['sub'],
            email=jwt_data['email'],
            phone_number=jwt_data['phone_number']
        )

        if user is None:
            msg = _('Invalid authorization header.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User inactive or deleted.')
            raise exceptions.AuthenticationFailed(msg)

        return (user, jwt_token)

    def authenticate_header(self, request):
        return 'Bearer: api'
