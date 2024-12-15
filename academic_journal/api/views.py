from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

from django.db.models import Q

from django.forms.models import model_to_dict

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer

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
from .serializers import CreateRankSerializer

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
                try:
                    lesson = Lesson.objects.get(date=date, order_in_day=order_in_day, semester=semester, subject=subject, teacher=user, group=group)
                    return Response({'Bad Request': 'This lesson is already exists!', 'lesson_id': lesson.id}, status=status.HTTP_400_BAD_REQUEST)
                except Lesson.DoesNotExist:
                    lesson = Lesson(date=date, order_in_day=order_in_day, semester=semester, subject=subject, teacher=user, group=group)
                    lesson.save()
                    return Response({'lesson_id': lesson.id}, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        current_visits = lesson.visits.all()
        for visit in request.data.get('visits'):
            student = Student.objects.get(id=visit['student_id'])
            if visit['visited']:
                if student not in current_visits:
                    lesson.visits.add(student)
            else:
                if student in current_visits:
                    lesson.visits.remove(student)
        lesson.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if request.GET.get('semester') and request.GET.get('group') and request.GET.get('subject'):
            queryset = self.get_queryset().filter(
                teacher=self.request.user,
                semester__id=request.GET.get('semester'),
                group__title=request.GET.get('group'),
                subject__title=request.GET.get('subject')
                ).order_by('-date', '-order_in_day')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = self.get_serializer(lesson)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.select_related('student', 'lesson')
    serializer_class = RankSerializer
    create_serializer_class = CreateRankSerializer
    filter_backends = (DjangoFilterBackend, )
    pagination_class = None

    def create(self, request, *args, **kwargs):
        for data in request.data.get('ranks'):
            serializer = self.create_serializer_class(data)
            lesson_id = data['lesson_id']
            student_id = data['student_id']
            rank = serializer.data.get('rank')
            try:
                rank_object = Rank.objects.get(lesson__id=lesson_id, student__id=student_id)
                if not rank:
                    rank_object.delete()
                    continue
                rank_object.rank = rank
            except Rank.DoesNotExist:
                if not rank:
                    continue
                rank_object = Rank(lesson=Lesson.objects.get(id=lesson_id), student=Student.objects.get(id=student_id), rank=rank)
            rank_object.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        if request.GET.get('lesson_id'):
            # Оценки за занятие
            lesson_id = int(request.GET.get('lesson_id'))
            queryset = self.get_queryset().filter(lesson__id=lesson_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.GET.get('semester_id') and request.GET.get('subject_title'):
            semester_id = int(request.GET.get('semester_id'))
            subject_title = request.GET.get('subject_title')
            if request.GET.get('student_id'):
                # Оценки одного студента по предмету за семестр
                student_id = request.GET.get('student_id')
                queryset = self.get_queryset().filter(student__id=student_id, lesson__semester__id=semester_id, lesson__subject__title=subject_title)
            elif request.GET.get('group_title'):
                # Оценки группы за весь семестр
                group_title = request.GET.get('group_title')
                queryset = self.get_queryset().filter(lesson__semester__id=semester_id, lesson__subject__title=subject_title, lesson__group__id=group_title)
            else:
                queryset = self.get_queryset().filter(lesson__semester__id=semester_id, lesson__subject__title=subject_title)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = (DjangoFilterBackend, )
    pagination_class = None

    def list(self, request, *args, **kwargs):
        if request.GET.get('group_title'):
            group_title = request.GET.get('group_title')
            queryset = self.get_queryset().filter(group__title=group_title).order_by("lastname")
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad request': 'group not specified'}, status=status.HTTP_400_BAD_REQUEST)
        

class GroupReportAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/group_report.html'

    def get(self, request):
        if request.GET.get('semester') and request.GET.get('group') and request.GET.get('subject'):
            semester = Semester.objects.get(id=int(request.GET.get('semester')))
            semester_name = f'{semester.semester_number}-й семестр, {semester.start_year}-{semester.end_year} уч. г.'
            
            lessons_queryset = Lesson.objects.filter(group__title=request.GET.get('group'), semester__id=request.GET.get('semester'), subject__title=request.GET.get('subject')).order_by('date', 'order_in_day')
            students_queryset = Student.objects.filter(group__title=request.GET.get('group'))
            students = StudentSerializer(students_queryset, many=True)
            lessons_ranks = dict()
            for lesson in lessons_queryset:
                lessons_ranks[lesson.id] = lesson.lesson_rank.all()

            lessons = []

            for lesson_id, lesson_ranks in lessons_ranks.items():
                lesson = model_to_dict(lessons_queryset.get(id=lesson_id))
                lesson['ranks'] = dict()

                for lesson_rank in lesson_ranks:
                    lesson['ranks'][lesson_rank.student.id] = model_to_dict(lesson_rank)['rank']

                if lesson['visits']:
                    visits = lesson['visits']
                    lesson['visits'] = []
                    for visit in visits:
                        visit = model_to_dict(visit)
                        lesson['visits'].append(visit['id'])
                
                format = "%m.%d.%Y"        
                lesson['date'] = lesson['date'].strftime(format)
                lessons.append(lesson)
                
        return Response({'lessons': lessons, 'students': students.data, 'group': request.GET.get('group'), 'subject': request.GET.get('subject'), 'semester': semester_name})
