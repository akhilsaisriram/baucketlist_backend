from datetime import datetime, timedelta
import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from members.models import User
from .models import Message

from .serialiser import Messageserialiser

from rest_framework import status
class peoples_on_samedate(APIView):
    def post(self, request):
        token = request.data.get('token')  # Use get method to avoid KeyError
        if not token:
            return Response({'error': 'Token is missing'}, status=400)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token is expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=401)

        user = User.objects.filter(uid=payload.get('gid')).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)

        current_user_bucket_list = user.bucket
        current_user_parsed_bucket_list = []
        
        for item in current_user_bucket_list:
            city = item.get('City')
            state = item.get('State')
            district = item.get('District')
            date_str = item.get('Date')
            
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    date = None
            else:
                date = None
            
            current_user_parsed_bucket_list.append({
                'City': city,
                'State': state,
                'District': district,
                'Date': date
            })
        
        # Find matching users
        matching_users = []
        
        for user_obj in User.objects.exclude(uid=user.uid):
            user_bucket_list = user_obj.bucket
            
            if user_bucket_list is None:
                continue
            
            for item in user_bucket_list:
                city = item.get('City')
                state = item.get('State')
                district = item.get('District')
                date_str = item.get('Date')
                
                if date_str:
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    except ValueError:
                        date = None
                else:
                    date = None
                
       
                for current_item in current_user_parsed_bucket_list:
                    if (
                        city == current_item['City'] and
                        state == current_item['State'] and
                        district == current_item['District'] and
                        date and current_item['Date'] and
                        abs((date - current_item['Date']).days) <= 2
                    ):
                        # Check if the user already exists in matching_users
                        user_found = False
                        for user in matching_users:
                            if user['id'] == user_obj.uid:
                                user['city'].append(city)
                                user['date'].append(date_str)
                                user_found = True
                                break
                        
                        # If user is not found, create a new object and append it to matching_users
                        if not user_found:
                            obj = {
                                'id': user_obj.uid,
                                'name': user_obj.name,
                                'city': [city],
                                'date': [date_str]
                            }
                            matching_users.append(obj)                       
                            
                        

        
        return Response({'matching_users': matching_users,"uid":payload.get('gid')}, status=200)



class Send_message(APIView):
    def post(self, request):
        token = request.data.get('token')
        room = request.data.get("room")
        print(room)
        if not token:
            return Response({'error': 'Token is missing'}, status=400)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token is expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=401)
        
        user = User.objects.filter(uid=payload.get('gid')).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)
        
        if not room:
            print("no data")
            return Response({'error': 'Message data is missing'}, status=400)
        
        message_room = Message.objects.filter(room=room).first()
        if not message_room:
            obj = {
                "room": room,
                "message": [{
                    "username": request.data.get("username"),
                    "message": request.data.get("message"),
                    "time": request.data.get("time")
                }]
            }
            print(obj)
            serializer = Messageserialiser(data=obj)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                error_message = "Invalid input. Please check your details."
                print(error_message)
                return Response({"error": error_message}, status=400)
        else:
            new_message = {
                "username": request.data.get("username"),
                "message": request.data.get("message"),
                "time": request.data.get("time")
            }
            if not isinstance(message_room.message, list):
                message_room.message = []
            message_room.message.append(new_message)
            message_room.save()
            return Response({"message": "Message added successfully"}, status=status.HTTP_200_OK)
        



class Get_message(APIView):
    def post(self, request):
        token = request.data.get('token')
        room = request.data.get("room")
        print(room)
        if not token:
            return Response({'error': 'Token is missing'}, status=400)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token is expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=401)
        
        user = User.objects.filter(uid=payload.get('gid')).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)
        
        if not room:
            print("no data")
            return Response({'error': 'Message data is missing'}, status=400)
        
        message_room = Message.objects.filter(room=room).first()
        print(message_room)
        serializer = Messageserialiser(message_room)
        return Response(serializer.data)