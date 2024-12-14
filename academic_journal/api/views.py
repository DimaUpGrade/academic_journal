from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

from django.db.models import Q

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, status, viewsets

from django_filters.rest_framework import DjangoFilterBackend

import rest_framework.permissions as perms

from .serializers import UserRegistrationSerializer
from .serializers import UserLoginSerializer
from .serializers import UsernameSerializer
from .serializers import LessonSerializer
from .serializers import GroupSerializer
from .serializers import RankSerializer
from .serializers import StudentSerializer
from .serializers import SubjectSerializer
from .serializers import SemesterSerializer
from .serializers import CreateLessonSerializer

from .models import Student
from .models import Group
from .models import Rank
from .models import Lesson
from .models import Subject
from .models import Semester


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
                return Response({'Token': Token.objects.get_or_create(user=user)[0].key, 'first_name': user.first_name, 'last_name': user.last_name}, status=status.HTTP_200_OK)
        return Response({"Error:": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [perms.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.filter(is_active=True).order_by('title')
    serializer_class = GroupSerializer
    filter_backends = (DjangoFilterBackend, )
    pagination_class = None


class SubjectListAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = (DjangoFilterBackend, )
    pagination_class = None
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({})
        else:
            queryset = self.get_queryset().filter(teachers__in=[user])
            serializer = self.get_serializer(queryset, many=True)
        
            return Response(serializer.data, status=status.HTTP_200_OK)


class SemesterListAPIView(generics.ListAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    filter_backends = (DjangoFilterBackend, )
    pagination_class = None

    def list(self, request, *args, **kwargs):
        year = datetime.now().year
        queryset = self.get_queryset().filter(Q(start_year=year) | Q(end_year=year))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    # Потестить отображение, семестр можно не возвращать обратно пользователю, как и группу
    queryset = Lesson.objects.select_related('semester', 'subject', 'group').prefetch_related('visits')
    serializer_class = LessonSerializer
    create_serializer_class = CreateLessonSerializer
    filter_backends = (DjangoFilterBackend, )

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = self.create_serializer_class(data=request.data)

            if serializer.is_valid():
                date = serializer.data.get('date')
                order_in_day = serializer.data.get('order_in_day')

                group_title = request.data["group"]
                subject_title = request.data["subject"]
                semester_id = int(request.data["semester_id"])
                
                group = Group.objects.get(title=group_title)
                subject = Subject.objects.get(title=subject_title)
                semester = Semester.objects.get(id=semester_id)

                lesson = Lesson(date=date, order_in_day=order_in_day, semester=semester, subject=subject, teacher=user, group=group)
                lesson.save()
                
                return Response(status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.GET.get('semester') and request.GET.get('group') and request.GET.get('subject'):
            queryset = self.get_queryset().filter(
                teacher=self.request.user,
                semester__id=request.GET.get('semester'),
                group__title=request.GET.get('group'),
                subject__title=request.GET.get('subject')
                ).order_by('-date')
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # def retrieve(self, request, *args, **kwargs):
    #     pk = self.kwargs.get("pk")
    #     lesson = get_object_or_404(Lesson, pk=pk)

        
        
        

