import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import ChatConsumer,ChatList
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hutoh.settings')
application = get_asgi_application()

ws_patterns = [
    path('ws/chat/<uuid:sender_id>/<uuid:receiver_id>/', ChatConsumer.as_asgi()),
    path('ws/chatlist/<uuid:user_id>/', ChatList.as_asgi()),
]

application= ProtocolTypeRouter({
    'http': application,
    'websocket': URLRouter(ws_patterns)
})