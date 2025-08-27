from django.conf import settings
from rest_framework import authentication, exceptions
from keycloak import KeycloakOpenID

# Get Keycloak configuration from Django settings
keycloak_config = settings.KEYCLOAK_CONFIG
keycloak_openid = KeycloakOpenID(
    server_url=keycloak_config['SERVER_URL'],
    client_id=keycloak_config['CLIENT_ID'],
    realm_name=keycloak_config['REALM']
)


class KeycloakUser:
    """
    Una classe wrapper per settare i flag corretti (altrimenti django si arrabbia)
    """

    def __init__(self, token_info):
        self.token_info = token_info

    @property
    def is_authenticated(self):
        return True

    # Allow dictionary-like access to the token claims for convenience.
    def __getitem__(self, key):
        return self.token_info[key]

    def get(self, key, default=None):
        return self.token_info.get(key, default)


class KeycloakAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the Bearer token from the Authorization header
        auth_header = authentication.get_authorization_header(request).split()

        print(request)

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None  # No token provided, anonymous request

        if len(auth_header) != 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Expected "Bearer <token>".')

        token = auth_header[1].decode('utf-8')

        try:
            # Decode the token. This will raise an exception if the token is invalid.
            token_info = keycloak_openid.decode_token(token)

            # If decoding is successful, authentication succeeds.
            # We return a tuple of (user, auth). DRF sets request.user to the first
            # element and request.auth to the second. We'll use the token payload for both.

            #creo un "utente" per django e lo ritorno
            user = KeycloakUser(token_info=token_info)

            return user, token_info

        except Exception as e:
            # Token is invalid, expired, or signature doesn't match
            raise exceptions.AuthenticationFailed(f'Token validation failed: {e}')