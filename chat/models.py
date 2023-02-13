import uuid
from django.db import models
from authentication.models import User

class Message(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    message = models.CharField(max_length=500)
    is_seen = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    