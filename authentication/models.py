import uuid, random
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    profile_pic = models.FileField(upload_to='static/profile/profile_pics',null=True,blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,unique=True)
    hutoh_id = models.CharField(max_length=150,unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.hutoh_id:
                self.hutoh_id = "DW" + str(random.randint(100000000000000, 999999999999999))
        super().save(*args, **kwargs)