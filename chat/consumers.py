import json
import base64
from io import BytesIO
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from channels.db import database_sync_to_async
from services.generator import CodeGenerator
from services.slugify import slugify
from services.exceptions import SendError
from django.contrib.auth import get_user_model

Users = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_code"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        user = self.scope['user']

        file = text_data_json.get('file', None)
        file_type = text_data_json.get('file_type', None)
        file_name = text_data_json.get('file_name', None)
        file_size = text_data_json.get('file_size', None)

        file_types = ['pdf', 'zip', 'rar', 'txt', 'doc', 'docx', 'rtf', 'xls',
                      'xlsx', 'ppt', 'pptx', 'png', 'jpeg', 'gif', 'jpg', 'mp4',
                      'avi', 'mkv', 'mov', 'mp3', 'mpeg', 'oog']

        if file:
            if file_type not in file_types:
                await self.send_error('FILE TYPE ERROR', 'This file format is not allowed')
            elif float(file_size) > 20.0:
                await self.send_error('FILE SIZE ERROR', 'This file size is not allowed')
            else:
                # Decode base64 file data to bytes
                decoded_file_data = base64.b64decode(file)

                file_name = slugify(file_name)

                file = decoded_file_data

                await self.database_message_operations(user, self.room_name, message, file, file_type, file_name, file_size)
        elif len(message) > 10000:
            await self.send_error('MESSAGE LENGTH ERROR', 'Message length should not exceed ten thousand characters')
        else:
            await self.database_message_operations(user, self.room_name, message, file, file_type, file_name, file_size)

        file_url = self.message_obj.file.url if self.message_obj.file else None
        get_file_name = self.message_obj.file_name if self.message_obj.file else None
        time = self.message_obj.get_time()
        data_id = self.message_obj.id

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message",
                                   "message": message,
                                   "user": user.username,
                                   "user_profile_photo": user.profile_photo.url,
                                   "file": file_url,
                                   "file_type": file_type,
                                   "file_name": get_file_name,
                                   "file_size": file_size,
                                   "time": time,
                                   "data_id": data_id
                                   }
                )

    async def send_error(self, code, message):
        await self.send(text_data=json.dumps({
            "error_type": "websocket.close",
            "error_code": code,
            "error_message": message
        }))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        user_profile_photo = event['user_profile_photo']
        file = event['file']
        file_type = event['file_type']
        file_name = event['file_name']
        file_size = event['file_size']
        time = event['time']
        data_id = event['data_id']


        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,
                                              "user": user,
                                              "user_profile_photo": user_profile_photo,
                                              "file": file,
                                              "file_type": file_type,
                                              "file_name": file_name,
                                              "file_size": file_size,
                                              "time": time,
                                              "data_id": data_id
                                              }))

    @database_sync_to_async
    def database_message_operations(self, user, room_code, message,  file, file_type, file_name, file_size):
        room = Room.objects.get(room_code=room_code)

        save_messsage = Message.objects.create(user=user, room=room, message=message, file_type=file_type,
                                               file_name=file_name, file_size=file_size)

        if file:
            file_io = BytesIO(file)
            file_name_generate = CodeGenerator.file_name_generator(size=20)

            save_messsage.file.save(f'{file_name_generate}.{file_type}', file_io)

        self.message_obj = save_messsage
