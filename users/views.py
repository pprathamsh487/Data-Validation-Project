from django.shortcuts import render

# Create your views here.
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from django.utils import timezone

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Manually update last_login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        })


class LogoutView(APIView):
    """
    Logout by deleting the user's token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Delete the current user's auth token
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)

