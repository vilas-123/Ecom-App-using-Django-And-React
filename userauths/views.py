from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from userauths.models import User,Profile
from userauths.serializer import MyTokenObtainPairSerializer,RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    query_set = User.objects.all()
    permission_changes =[AllowAny]
    serializer_class = RegisterSerializer