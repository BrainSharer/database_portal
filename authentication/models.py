from django.db import models
from django.contrib.auth.models import AbstractUser

class Lab(models.Model):
    id = models.AutoField(primary_key=True)
    lab_name = models.CharField(max_length=100, blank=False, null=False)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        verbose_name = 'Laboratory'
        verbose_name_plural = 'Labs'
        
    def __str__(self):
        return f"{self.lab_name}"

class User(AbstractUser):
    labs = models.ManyToManyField(Lab, related_name="labs")
    
    
    
