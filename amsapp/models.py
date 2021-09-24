from django.contrib.auth.models import User
from django.db import models
import datetime


# Create your models here.




class Institute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    alias = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=1)


class Department(models.Model):
    institute_id = models.ForeignKey(Institute, related_name='department', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    alias = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=1)


class Semester(models.Model):
    sem_in_number = models.IntegerField()
    sem_in_roman = models.CharField(max_length=10)
    status = models.IntegerField(default=1)


class Branch(models.Model):
    name = models.CharField(max_length=20, unique=True)
    alias = models.CharField(max_length=20, unique=True, null=True)
    dept_id = models.ForeignKey(Department, related_name='branch', on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=1)


class Attendence(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    user_semester_id=models.IntegerField(default=1)


class ExtendedUsers(models.Model):
    # fname = models.CharField(max_length=100)
    org_password = models.CharField(max_length=100, default="1234")
    branch = models.ForeignKey(Branch,related_name='branch',on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    user_role = models.CharField(max_length=10)
    # registration_date = models.DateField(("registration_date"), default=datetime.date.today())
    user = models.OneToOneField(User, related_name='info', on_delete=models.CASCADE)
    sem_id = models.ForeignKey(Semester,related_name='semester',on_delete=models.CASCADE)
    disp=models.CharField(max_length=100,null=True)
    user_status = models.IntegerField(default=1)
    updated_on = models.DateField(("updated_on"), default=datetime.date.today())