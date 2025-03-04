# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# import json
# class TestConsumer(WebsocketConsumer):


#     def connect(self):
#         self.room_name="test_consumer"
#         self.room_group_name="test_consumer_group"
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_name,self.room_group_name
#         )
#         self.accept()
#         self.send(text_data=json.dumps({'status':'connected from django channels'}))

#     def receive(self,text_data):
#         print(text_data)

#         self.send(text_data=json.dumps({'status':'we got ur data from front end'}))

#     def disconnect(self,*args, **kwargs):
#         print("disconnected")

import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Message
# room_name
# class TestConsumer(AsyncWebsocketConsumer):
#     users_in_room = {} 
#     async def connect(self):
#         self.room_name=self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name= "chat_%s" % self.room_name
#         self.username=self.scope["url_route"]["kwargs"]["username"]
#         print(self.username)
#         print(self.room_name)
#         print(self.room_group_name)
#         # Join room
#         if self.room_group_name not in TestConsumer.users_in_room:
#             TestConsumer.users_in_room[self.room_group_name] = set()
#         TestConsumer.users_in_room[self.room_group_name].add(self.username)
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
#             }
#         )

#     async def disconnect(self, close_code):
#         # Leave room
#         if self.room_group_name in TestConsumer.users_in_room:
#             TestConsumer.users_in_room[self.room_group_name].discard(self.username)

#         await self.channel_layer.group_discard(
            
#             self.room_group_name,
#             self.channel_name
#         )
#         # Notify the room group that a user has left
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'user_leave',
#                 'username': self.username,
#             }
#         )


#     # Receive message from web socket
#     async def receive(self, text_data):
#         data = json.loads(text_data)

#         # print(data)
#         message = data.get('message')
#         username = data['username']
#         room = data['room']
#         time=data['time']
#         # await self.save_message(username, room, message)
   
        
#         if time == 'get_user_count':
#             await self.send_user_count()
#         # Send message to room group

#         elif(time=="username_type"):
#             try:
#                 await self.channel_layer.group_send(
#                 self.room_group_name,
#                {
#                    'type': 'typeing',
#                    'message': message,
#                    'username': username,
                   
#                }
#             )
#             except Exception as e:
#              print(f"Error sending binary data rr: {str(e)}") 
             
#         else:
#             try:
#                 await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_message',
#                     'message': message,
#                     'username': username,
#                     'time':time,
#                 }
#             )

#             except Exception as e:
#                 print(f"Error sending binary data rr: {str(e)}")
            
    
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']
#         time = event['time']
#         # Send message to WebSocket
       
        
#         try:
#             # Decode the base64 data to bytes
         
#             print(message,time)
#             # Send the binary data as-is
#             await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username,
#             'time':time,
#         }))
#             from datetime import datetime

#             now = datetime.now()

#             current_time = now.strftime("%H:%M:%S")
#             print("Current Time =", current_time)
            
#             await self.send(text_data=json.dumps({
#             'type': 'acknowledge',
#             'message': 'Message received and acknowledged.',
#         }))
#         except Exception as e:
#             print(f"Error sending binary data: {str(e)}")



#     async def typeing(self, event):
#         username = event['username']
#         message=event['message']
#         print("typeing",message,username)
#         # Send a user join notification to the WebSocket
#         await self.send(text_data=json.dumps({
#             'message': username,
#             'stat':message,
#             'username': 'typeing',
#         }))


#     # Notify the room group that a user has joined
#     async def user_join(self, event):
#         username = event['username']

#         # Send a user join notification to the WebSocket
#         await self.send(text_data=json.dumps({
#             'message': f'{username} has joined the room.',
#             'username': 'system',
#         }))

#     # Notify the room group that a user has left
#     async def user_leave(self, event):
#         username = event['username']

#         # Send a user leave notification to the WebSocket
#         await self.send(text_data=json.dumps({
#             'message': f'{username} has left the room.',
#             'username': 'system',
#         }))


#     async def send_user_count(self):
#         user_count = len(TestConsumer.users_in_room.get(self.room_group_name, []))
#         await self.send(text_data=json.dumps({
#             'type': 'user_count',
#             'count': user_count,
#         }))
#     @sync_to_async
#     def save_message(self, username, room, message):
#         Message.objects.create(username=username, room=room, content=message)

class TestConsumer(AsyncWebsocketConsumer):
    users_in_room = {}  # Class attribute to track users in rooms

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.username = self.scope["url_route"]["kwargs"]["username"]

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

        elif message_type=='typing':
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

        else:
            message = data.get('message')
            username = data['username']  
            time = data['time']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'time': time,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        time = event['time']
        # Send message to WebSocket       
        try:
            await self.send(text_data=json.dumps({
            'message': message,
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
    
    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)
