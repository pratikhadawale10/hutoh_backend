from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    profile_pic = models.FileField(upload_to='static/profile/profile_pics',null=True,blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)