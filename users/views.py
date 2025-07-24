from django.shortcuts import render

# Create your views here.
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

from rest_framework import generics


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]




