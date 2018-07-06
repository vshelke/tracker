from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class User(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    thumbnail = models.URLField()
    user_type = models.CharField(max_length=20)
    fullname = models.CharField(max_length=60, null=True)
    email = models.EmailField(unique=True, null=True)
    location = models.CharField(max_length=80, null=True)
    created = models.DateTimeField()
    followers = models.PositiveIntegerField()
    languages = ArrayField(models.CharField(max_length=50, blank=True))
