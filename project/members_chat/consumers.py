

# import json
# import base64
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async

# from .models import Message
# from encrypt import  encrypt_data, decrypt_data

# class TestConsumer(AsyncWebsocketConsumer):
#     users_in_room = {}  # Class attribute to track users in rooms

#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
#         self.username = self.scope["url_route"]["kwargs"]["username"]

#         # Add user to the room's user list
#         if self.room_group_name not in TestConsumer.users_in_room:
#             TestConsumer.users_in_room[self.room_group_name] = set()
#         TestConsumer.users_in_room[self.room_group_name].add(self.username)

#         # Join room
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#         # Notify the room group that a new user has joined
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'user_join',
#                 'username': self.username,
#                 'online_users': list(TestConsumer.users_in_room[self.room_group_name]),
#             }
#         )

#     async def disconnect(self, close_code):
#         # Remove user from the room's user list
#         print("dis")
#         if self.room_group_name in TestConsumer.users_in_room:
#             TestConsumer.users_in_room[self.room_group_name].discard(self.username)

#         # Notify the room group that a user has left
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'user_leave',
#                 'username': self.username,
#                 'online_users': list(TestConsumer.users_in_room[self.room_group_name]),
#             }
#         )

#         # Leave room
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from web socket
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get('type')
        
#         if message_type == 'get_user_count':
#             await self.send_user_count()

#         elif message_type=='typing':
#             message = data.get('message')
#             username = data['username']         
          
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'typing',
#                     'message': message,
#                     'username': username,
#                 }
#             )
#         elif message_type == 'notify':
#             notification = data.get('notification')
#             print(notification)
#             await self.notify_all(notification)

#         else:
#             message = data.get('message')
#             username = data['username']  
#             time = data['time']
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_message',
#                     'message': message,
#                     'username': username,
#                     'time': time,
#                 }
#             )

#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']
#         time = event['time']

#         # Send message to WebSocket       
#         try:
#             await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username,
#             'time': time,
#         }))
            
#             await self.send(text_data=json.dumps({
#             'type': 'acknowledge',
#             'message': 'Message received and acknowledged.',
#         }))
#         except Exception as e:
#             print(f"Error sending message: {str(e)}")

#     async def typing(self, event):
#         username = event['username']
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'username': username,
#             'message': message,
#             'type': 'typing',
#         }))

#     async def user_join(self, event):
#         username = event['username']
#         online_users = event['online_users']
#         await self.send(text_data=json.dumps({
#             'username': username,
#             'type': 'user_join',
#             'online_users': online_users,
#         }))

#     async def user_leave(self, event):
#         username = event['username']
#         online_users = event['online_users']
#         await self.send(text_data=json.dumps({
#             'username': username,
#             'type': 'user_leave',
#             'online_users': online_users,
#         }))

#     async def send_user_count(self):
#         user_count = len(TestConsumer.users_in_room.get(self.room_group_name, []))
#         await self.send(text_data=json.dumps({
#             'type': 'user_count',
#             'count': user_count,
#         }))

#     async def notify_all(self, notification):
#         # Broadcast the notification to all users in all rooms
#         for room_group_name in TestConsumer.users_in_room.keys():
#             await self.channel_layer.group_send(
#                 room_group_name,
#                 {
#                     'type': 'notification',
#                     'notification': notification,
#                 }
#             )

#     async def notification(self, event):
#         notification = event['notification']
#         # Send the notification to WebSocket
#         print(notification)
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'notification': notification,
#         }))


#     @sync_to_async
#     def save_message(self, username, room, message):
#         Message.objects.create(username=username, room=room, content=message)
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Message
from .encrypt import encrypt_data, decrypt_data

class TestConsumer(AsyncWebsocketConsumer):
    users_in_room = {}  # Class attribute to track users in rooms

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.username = self.scope["url_route"]["kwargs"]["username"]
        # print("room",self.room_name)
        # Add user to the room's user list
        if self.room_group_name not in TestConsumer.users_in_room:
            TestConsumer.users_in_room[self.room_group_name] = set()
        TestConsumer.users_in_room[self.room_group_name].add(self.username)

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Notify the room group that a new user has joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.username,
                'online_users': list(TestConsumer.users_in_room[self.room_group_name]),
            }
        )

    async def disconnect(self, close_code):
        # Remove user from the room's user list
        print("dis")
        if self.room_group_name in TestConsumer.users_in_room:
            TestConsumer.users_in_room[self.room_group_name].discard(self.username)

        # Notify the room group that a user has left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.username,
                'online_users': list(TestConsumer.users_in_room[self.room_group_name]),
            }
        )

        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'get_user_count':
            await self.send_user_count()

        elif message_type == 'typing':
            message = data.get('message')
            username = data['username']         
          
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing',
                    'message': message,
                    'username': username,
                }
            )
        elif message_type == 'notify':
            notification = data.get('notification')
            print(notification)
            await self.notify_all(notification)

        else:
            message = data.get('message')
            username = data['username']  
            time = data['time']
            
            # Encrypt the message
            key = self.room_name  # Use your key here
            encrypted_message = encrypt_data(key, message.encode('utf-8'))
            print(encrypted_message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': encrypted_message,
                    'username': username,
                    'time': time,
                }
            )

    async def chat_message(self, event):
        encrypted_message = event['message']
        username = event['username']
        time = event['time']
        
        # Decrypt the message
        key =self.room_name  # Use your key here
        decrypted_message = decrypt_data(key, encrypted_message).decode('utf-8')
        
        # Send message to WebSocket       
        try:
            await self.send(text_data=json.dumps({
                'message': decrypted_message,
                'username': username,
                'time': time,
            }))
            
            await self.send(text_data=json.dumps({
                'type': 'acknowledge',
                'message': 'Message received and acknowledged.',
            }))
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    async def typing(self, event):
        username = event['username']
        message = event['message']
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message,
            'type': 'typing',
        }))

    async def user_join(self, event):
        username = event['username']
        online_users = event['online_users']
        await self.send(text_data=json.dumps({
            'username': username,
            'type': 'user_join',
            'online_users': online_users,
        }))

    async def user_leave(self, event):
        username = event['username']
        online_users = event['online_users']
        await self.send(text_data=json.dumps({
            'username': username,
            'type': 'user_leave',
            'online_users': online_users,
        }))

    async def send_user_count(self):
        user_count = len(TestConsumer.users_in_room.get(self.room_group_name, []))
        await self.send(text_data=json.dumps({
            'type': 'user_count',
            'count': user_count,
        }))

    async def notify_all(self, notification):
        # Broadcast the notification to all users in all rooms
        for room_group_name in TestConsumer.users_in_room.keys():
            await self.channel_layer.group_send(
                room_group_name,
                {
                    'type': 'notification',
                    'notification': notification,
                }
            )

    async def notification(self, event):
        notification = event['notification']
        # Send the notification to WebSocket
        print(notification)
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification,
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)
