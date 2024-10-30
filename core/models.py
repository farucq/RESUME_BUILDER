
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Cv(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    cv = models.ForeignKey(Cv, on_delete = models.CASCADE)
    s_name = models.CharField(max_length=500)
    s_level = models.CharField(max_length=500)

    def __str__(self):
        return self.s_name


class Academic(models.Model):
    cv = models.ForeignKey(Cv, on_delete = models.CASCADE)
    a_institution = models.CharField(max_length=500)
    a_year = models.CharField(max_length=500)
    a_award = models.CharField(max_length=500)

    def __str__(self):
        return self.a_institution

class Experience(models.Model):
    cv = models.ForeignKey(Cv, on_delete = models.CASCADE)
    e_name = models.CharField(max_length=500)
    e_role = models.CharField(max_length=500)
    e_duration = models.CharField(max_length=500)

    def __str__(self):
        return self.e_name

class Referee(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    re_name = models.CharField(max_length=500)
    re_email = models.CharField(max_length=500)
    re_phone = models.CharField(max_length=500)

    def __str__(self):
        return self.re_name


class Profile(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    fname = models.CharField(max_length=500)
    lname = models.CharField(max_length=500)
    mname = models.CharField(max_length=500)
    gender = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    region = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    occupation = models.CharField(max_length=500)
    dob = models.DateField(default='None')
    bio = models.TextField()
    avator = models.ImageField(upload_to='profile/', default='profile/avator.png', null=True)

    def __str__(self):
        return self.fname

    def delete(self, *args, **kwargs):
        self.avator.delete()
        super().delete(*args, **kwargs)

from django.utils import timezone


class Feedback(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback from {self.username} on {self.created_at}"