import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import logging
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import ChatRoom, Message

logger = logging.getLogger(__name__)
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        logger.info(f"WebSocket connected to room ID: {self.room_id}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        user = await self.save_message(username, message)

        if user:
            user_info = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'avatar': user.avatar.url if user.avatar and hasattr(user.avatar, 'url') else None
            }
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user_info
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        await self.send(text_data=json.dumps({'message': message, 'user': user}))

    @database_sync_to_async
    def save_message(self, username, content):
        try:
            user = User.objects.get(username=username)
            room = ChatRoom.objects.get(id=self.room_id)
            Message.objects.create(room=room, sender=user, content=content, timestamp=timezone.now())
            return user
        except ObjectDoesNotExist as e:
            logger.error(f"Error saving message: {e}")
            return None
