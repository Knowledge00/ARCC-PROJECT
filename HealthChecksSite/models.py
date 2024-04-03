from django.db import models

# Create your models here.

class SignIn(models.Model):
    Name = models.CharField(max_length=500, unique=True)
    Password = models.CharField(max_length=500,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.name 
