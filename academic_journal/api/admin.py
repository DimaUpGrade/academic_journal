from django import forms
from django.contrib import admin
from .models import Student
from .models import Group
from .models import Rank
from .models import Lesson
from .models import Subject
from .models import Semester


class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'group', 'date', 'teacher', 'semester', )
    list_display_links = ('subject', )
    list_filter = ('group', 'teacher', 'semester', 'subject', )
    search_fields = ('subject__title__startswith', )

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "visits":
    #         # print("asdfadasdsa")
    #         kwargs["queryset"] = Student.objects.filter(group__title="ИТ2442")
    #         return super().formfield_for_manytomany(db_field, request, **kwargs)
    #     if db_field.name == "ranks":
    #         # kwargs["queryset"] = Lesson.objects.get(pk=self.kwargs.get('pk')).ranks.all()

    #         return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Rank)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Subject)
admin.site.register(Semester)
