from django.contrib import admin
from chat.models import Message,ChatMessage,ChatRoom

admin.site.register(Message)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)