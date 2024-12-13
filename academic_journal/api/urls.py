from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('login/', UserLogin.as_view(), name='login'),
    path('is_username_taken/', IsUsernameTaken.as_view(), name='is_username_taken'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('groups/', GroupListAPIView.as_view(), name='groups'),
    path('subjects/', SubjectListAPIView.as_view(), name='subjects'),
    path('semesters/', SemesterListAPIView.as_view(), name='semesters'),
]