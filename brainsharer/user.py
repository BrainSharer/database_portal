# authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    labs = models.ManyToManyField('self',)
