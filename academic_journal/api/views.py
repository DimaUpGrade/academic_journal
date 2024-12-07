from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, status, viewsets

import rest_framework.permissions as perms

from serializers import UserRegistrationSerializer
from serializers import UserLoginSerializer
from serializers import UsernameSerializer
from serializers import LessonSerializer

from models import Student
from models import Group
from models import Rank
from models import Lesson
from models import Subject


class UserRegistration(APIView):
    permission_classes = [perms.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'Bad request': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class IsUsernameTaken(APIView):
    permission_classes = [perms.AllowAny]
    serializer_class = UsernameSerializer

    def post(self, request):
        serializer = UsernameSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"Username is valid": "Username is valid"}, status=status.HTTP_200_OK)
        return Response({"Username is taken": "Username is taken or something wrong"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [perms.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = serializer.check_user(request.data)
            except:
                return Response({"Bad request:": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            if user:
                login(request, user)
                return Response({'Token': Token.objects.get_or_create(user=user)[0].key}, status=status.HTTP_200_OK)
        return Response({"Error:": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [perms.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
