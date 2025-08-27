from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])  # No token required
@authentication_classes([])  # No authentication will be performed
def public_view(request):
    """
    An endpoint that is open to the public and requires no authentication.
    """
    return Response({"message": "This is a public endpoint. Anyone can see this!"})


@api_view(['GET'])
# Default authentication and permission classes from settings.py are used here
def protected_view(request):
    """
    A protected endpoint that requires a valid Keycloak JWT.
    The user's info is populated by the KeycloakAuthentication class.
    """
    # The `request.user` object is a KeycloakUser instance, used for permission checks.
    # The `request.auth` object holds the raw token claims (the dictionary).

    # **FIX:** We use `request.auth` in the response body because it's a dictionary
    # and is already JSON serializable. Using `request.user` would cause a TypeError.
    user_claims = request.auth

    return Response({
        "message": f"Hello, {request.user.get('preferred_username', 'user')}! This is a protected endpoint.",
        "user_details": user_claims,
    })