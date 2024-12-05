from rest_framework import serializers
from .models import Teacher
from .models import Student
from .models import Group
from .models import Rank
from .models import Lesson
from .models import Subject
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError


