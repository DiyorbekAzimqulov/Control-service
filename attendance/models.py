from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Just customizing default django's user model"""
    pass


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class Employee(models.Model):
    unique_id = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='attendance/employees')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class ComeIn(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class ComeOut(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)


class DaySummary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    come_in = models.ForeignKey(ComeIn, on_delete=models.CASCADE)
    come_out = models.ForeignKey(ComeOut, on_delete=models.CASCADE)
    total_work_hours = models.DateTimeField(null=True, blank=True)
