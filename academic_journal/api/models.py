from django.db import models


#
# Default Django User model (i.e. auth.models.User class)
# has atributes:
#
# username
# email
# first_name
# last_name
# date_joined
# last_login
#

# class Teacher(models.Model):
#     email = models.EmailField()
#     firstname = models.CharField()
#     lastname = models.CharField()
#     secondname = models.CharField(null=True, blank=True)
#     user = models.ForeignKey("auth.User", related_name="user_teacher")

#     def __str__(self):
#         return f"{self.firstname} {self.lastname} {self.secondname}"


class Group(models.Model):
    title = models.CharField(max_length=10) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Subject(models.Model):
    title = models.CharField(max_length=60)
    teachers = models.ManyToManyField("auth.User", related_name="subject_teachers")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    date = models.DateField()
    order_in_day = models.IntegerField()
    semester = models.ForeignKey("Semester", related_name="semester_lesson", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", related_name="subject_lesson", on_delete=models.CASCADE)
    teacher = models.ForeignKey("auth.User", related_name="teacher_lesson", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", related_name="group_lesson", on_delete=models.CASCADE)
    visits = models.ManyToManyField("Student", blank=True, related_name="lesson_visits")

    def __str__(self):
        return f"{self.date}, {self.order_in_day} пара, {self.subject.title}, {self.group.title}"


class Student(models.Model):
    firstname = models.CharField()
    lastname = models.CharField()
    secondname = models.CharField(null=True, blank=True)
    group = models.ForeignKey("Group", related_name="group_student", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.secondname}"


class Rank(models.Model):
    lesson = models.ForeignKey("Lesson", related_name="lesson_rank", on_delete=models.CASCADE, default=None)
    student = models.ForeignKey("Student", related_name="student_rank", on_delete=models.CASCADE)
    rank = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student}, {self.rank}"
    

class Semester(models.Model):
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    semester_number = models.IntegerField()

    def __str__(self):
        return f"{self.start_year}-{self.end_year}, {self.semester_number}-й семестр"
