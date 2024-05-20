# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import Message, ChatRoom, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        username = text_data_json['username']  # Giả sử bạn gửi username từ frontend

        # Lưu tin nhắn vào cơ sở dữ liệu
        try:
            user = await User.objects.get(username=username)
            room = await ChatRoom.objects.get(name=self.room_name)
            message = await Message.objects.create(
                room=room,
                sender=user,
                content=message_content
            )
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'username': username,
                    'timestamp': str(message.timestamp)
                }
            )
        except User.DoesNotExist:
            print(f"User with username {username} does not exist.")
        except ChatRoom.DoesNotExist:
            print(f"Chat room with name {self.room_name} does not exist.")

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
