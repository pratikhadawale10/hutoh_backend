import json
from channels.generic.websocket import AsyncWebsocketConsumer
from authentication.models import User
from chat.models import Message
from asgiref.sync import sync_to_async
from django.db import models

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
