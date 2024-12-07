from django.db import models


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

    def __str__(self):
        return self.title


class Subject(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    date = models.DateField()
    order_in_day = models.IntegerField(max_length=1)
    subject = models.ForeignKey("Subject", related_name="subject_lesson")
    # teacher = models.ForeignKey("Teacher", related_name="teacher_lesson")
    teacher = models.ForeignKey("auth.User", related_name="teacher_lesson")
    group = models.ForeignKey("Group", related_name="group_lesson")
    visits = models.ManyToManyField("Student", blank=True, related_name="lesson_visits")
    ranks = models.ManyToManyField("Rank", blank=True, related_name="lesson_ranks")

    def __str__(self):
        return f"{self.date}, {self.order_in_day}"


class Student(models.Model):
    firstname = models.CharField()
    lastname = models.CharField()
    secondname = models.CharField(null=True, blank=True)
    group = models.ForeignKey("Group", related_name="group_student")

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.secondname}"


class Rank(models.Model):
    student = models.ForeignKey("Student", related_name="student_rank")
    rank = models.IntegerField(max_length=1)

    def __str__(self):
        return f"{self.student}, {self.rank}"
