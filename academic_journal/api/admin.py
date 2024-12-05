from django.contrib import admin
from .models import Teacher
from .models import Student
from .models import Group
from .models import Rank
from .models import Lesson
from .models import Subject


admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Rank)
admin.site.register(Lesson)
admin.site.register(Subject)
