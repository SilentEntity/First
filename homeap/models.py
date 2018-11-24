from django.db import models

# Create your models here.
from djongo import models

class Users(models.Model):            #this is collection name
    username=models.CharField(max_length=25)
    password=models.CharField(max_length=25)
    follower=models.ListField(default=[1,2])
    following=models.ListField(default=[1,2])



