import json
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import User
from chat.models import Message
from asgiref.sync import sync_to_async, async_to_sync
from django.db import models
from django.db.models import Q
from django.db.models import Case, IntegerField, F, When
from .models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user IDs for the sender and receiver from the URL path.
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']

        # Check that the sender and receiver are valid users.
        try:
            self.sender = await sync_to_async(User.objects.get)(id=self.sender_id)
            self.receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)
        except User.DoesNotExist:
            await self.close()

        # Join the channel group for this chat.
        chat_group_ids = sorted([self.sender_id, self.receiver_id])
        self.chat_group_name = f'chat_{chat_group_ids[0]}_{chat_group_ids[1]}'
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

        messages = await sync_to_async(Message.objects.filter)(
            (models.Q(sender=self.sender) & models.Q(receiver=self.receiver)) |
            (models.Q(sender=self.receiver) & models.Q(receiver=self.sender))
        )
        async for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.message,
                'sender_id': str(message.sender_id),
                'timestamp': str(message.created_at)
            }))


    async def disconnect(self, close_code):
        # Leave the channel group.
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Save the message to the database.
        message = await sync_to_async(Message.objects.create)(
            sender=self.sender,
            receiver=self.receiver,
            message=text_data
        )

        # Broadcast the message to everyone in the chat group.
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message.message,
                'sender_id': str(message.sender_id),
                'timestamp': str(message.created_at)
            }
        )

    async def chat_message(self, event):
        # Send the message to the WebSocket.
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp']
        }))





class ChatList(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user id from the query string
        self.user_id = self.scope['url_route']['kwargs']['user_id']
         # Get the chat room name from the URL
        self.room_name = 'chat_%s' % self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = self.room_name
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        chat_rooms = await self.get_chat_rooms()
        await self.send(text_data=chat_rooms)


    async def receive(self, text_data):
        chat_rooms = await self.get_chat_rooms()
        await self.send(text_data=chat_rooms)


    async def update_chat_list(self, message):
        text = message.get('text_data', '')
        await self.send(text_data=text)


    async def disconnect(self, close_code):
        # Leave the group for this user's chat list
        await self.channel_layer.group_discard(
            'chat_list_{}'.format(self.user_id),
            self.channel_name,
        )
    

    @sync_to_async
    def get_chat_rooms(self):
        chat_rooms = ChatRoom.objects.filter(users__id=self.user_id)
        chat_list = []
        for room in chat_rooms:
            messages = ChatMessage.objects.filter(chat=room).order_by("timestamp")
            other_user = room.users.exclude(id=self.user_id).first()
            if ChatMessage.objects.filter(chat=room):
                print("hello")
                last_message = messages.last()
                unread_count = room.messages.filter(sender=other_user, is_seen=False).count()
                chat_room_data = {
                    'room_id': str(room.room_id),
                    'current_user_id': str(self.user_id),
                    'other_user_id': str(other_user.id),
                    'other_user_name': other_user.username,
                    'unread_count': unread_count,
                    'last_message':{
                        'sender': str(last_message.sender.id),
                        'is_seen': last_message.is_seen,
                        'content': last_message.content,
                        'timestamp': str(last_message.timestamp),
                        'room_id': str(last_message.chat.room_id),
                    }
                }
                chat_list.append(chat_room_data)
        return json.dumps(chat_list)
