import uuid
from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
import json

class Message(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    message = models.CharField(max_length=500)
    is_seen = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    

class ChatRoom(models.Model):
    room_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    users = models.ManyToManyField(User, related_name='chats')
    def clean(self):
        # Ensure that the combination of users in the chat room is unique
        if ChatRoom.objects.filter(users__in=self.users.all()).distinct().count() > 1:
            raise ValidationError('This combination of users is already in a chat room.')



class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(str(self.timestamp))
        users = users = self.chat.users.all()
        for user in users:
            user_id = str(user.id)
            
            chat_list = []
            chat_rooms = ChatRoom.objects.filter(users__id=user_id)
            for room in chat_rooms:
                other_user = room.users.exclude(id=user_id).first()
                if room == self.chat:
                    if self.sender != user:
                        unread_count = ChatMessage.objects.filter(chat=room,sender=other_user,is_seen=False).count()
                    else:
                        unread_count = 0
                    chat_room_data = {
                        'room_id': str(room.room_id),
                        'current_user_id': user_id,
                        'other_user_id': str(other_user.id),
                        'other_user_name': other_user.username,
                        'unread_count': unread_count,
                        'last_message':{
                            'sender': str(self.sender.id),
                            'is_seen': self.is_seen,
                            'content': self.content,
                            'timestamp': str(self.timestamp),
                            'room_id': str(self.chat.room_id),
                        }
                    }
                    chat_list.append(chat_room_data)
                else:
                    unread_count = ChatMessage.objects.filter(chat=room,sender=other_user,is_seen=False).count()
                    messages = ChatMessage.objects.filter(chat=room).order_by("timestamp")
                    if messages:
                        chat_room_data = {
                                'room_id': str(room.room_id),
                                'current_user_id': user_id,
                                'other_user_id': str(other_user.id),
                                'other_user_name': other_user.username,
                                'unread_count': unread_count,
                                'last_message':{
                                    'sender': str(messages.last().sender.id),
                                    'is_seen': messages.last().is_seen,
                                    'content': messages.last().content,
                                    'timestamp': str(messages.last().timestamp),
                                    'room_id': str(messages.last().chat.room_id),
                                }
                            }
                        chat_list.append(chat_room_data)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{user_id}',
                {
                    'type': 'update_chat_list',
                    'text_data': json.dumps(chat_list),
                }
            )


            

            
        