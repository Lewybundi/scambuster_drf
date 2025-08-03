from rest_framework.decorators import api_view
from .serializer import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from user_app.models import create_auth_token
@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data= request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token,_ = Token.objects.get_or_create(user=user)
    return Response({
    'Response': 'Successfully registered',
     'username': user.username,
     'email':user.email,
     'token': token.key
    })
    
@api_view(["POST"])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)