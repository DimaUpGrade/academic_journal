from rest_framework import serializers
from .models import Student
from .models import Group
from .models import Rank
from .models import Lesson
from .models import Subject
from .models import Semester
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_obj = User.objects.create_user(email=validated_data['email'], username=validated_data['username'],
                                            password=validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user_obj.save()
        token = Token.objects.create(user=user_obj)
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise ValidationError('User not found.')
        return user


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title',)

    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        group = GroupSerializer(many=False, read_only=False)
        fields = ('firstname', 'lastname', 'group')
        

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'title',)


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        visits = StudentSerializer(many=True, read_only=False)
        teacher = UserFullSerializer(many=False, read_only=False)
        subject = SubjectSerializer(many=False, read_only=False)
        fields = ("id", "teacher", "subject", "visits", "date", "order_in_day")

        
class CreateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        subject = SubjectSerializer(many=False, read_only=False)
        fields = ("teacher", "subject", "date", "order_in_day")


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"


# class CreateRankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rank
#         student = Student
#         fields = ("rank", "student")
        

