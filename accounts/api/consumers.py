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
        logger.info("WebSocket connected")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info(f"Received data: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']  # Ensure this is being sent from the client

        # Save the message to the database asynchronously
        await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, username, content):
        try:
            user = User.objects.get(username=username)
            room = ChatRoom.objects.get(name=self.room_name)
            Message.objects.create(room=room, sender=user, content=content, timestamp=timezone.now())
        except ObjectDoesNotExist as e:
            logger.error(f"Error saving message: {e}")
            # Handle the error appropriately, possibly notifying the user
            # For instance, you could raise an exception or return a specific message
            return False
