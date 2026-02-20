# Authentication and Permissions

This API uses TokenAuthentication provided by Django REST Framework.

Authentication Setup:
- Added 'rest_framework.authtoken' to INSTALLED_APPS
- Configured DEFAULT_AUTHENTICATION_CLASSES to use TokenAuthentication
- Configured DEFAULT_PERMISSION_CLASSES to require IsAuthenticated

Token Retrieval:
Users obtain a token by sending a POST request to:

/api/token/

With:
{
  "username": "username",
  "password": "password"
}

Authenticated Requests:
Include the token in the Authorization header:

Authorization: Token <your_token>

Permissions:
BookViewSet requires authentication using:
permission_classes = [IsAuthenticated]

