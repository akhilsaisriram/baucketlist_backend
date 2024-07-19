from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serialiser import UserSerializer
from .models import User
from members.models import User as uu
import jwt, datetime
from rest_framework import status
import cv2
import numpy as np
from openai import OpenAI

# Create your views here.


class ChatgptView(APIView):
    def post(self, request):
        input_text = request.data.get('input', '')  # Using get to handle cases when input is not provided
        openai = OpenAI(
            api_key='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',
        )
        try:
            template = f"""
            You are chatting with a plant disease information system. Your goal is to clear the user's doubts and provide answers concisely, in less than 100 words.

            Begin!

            User Input:
            {input_text}
            """

            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": template},
                ]
            )

            response = completion.choices[0].message.content
            print({"output": response})

            # Return the response using Response object
            return Response({"output": response})  # Response data wrapped in a dictionary

        except Exception as e:
            print({"error": str(e)})
            # Return an error response if an exception occurs
            return Response({"error": str(e)}, status=500)  # Internal Server Error status code


class FeedView(APIView):
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

        user = uu.objects.filter(uid=payload.get('gid')).first()

        if not user:
            return Response({'error': 'User not found'}, status=404)
        
        feed = User.objects.all()
        serializer = UserSerializer(feed, many=True) 
        return Response(serializer.data)


###############################################user based############################################

from rest_framework.parsers import MultiPartParser
import base64

class Add_bucket_feed(APIView):

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')  # Retrieve the token from the request
        data = request.data.copy()
        if not token:
            return Response({'error': 'Token is missing'}, status=400)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token is expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=401)
        data['userid']=payload.get('gid')
        user = uu.objects.filter(uid=payload.get('gid')).first()
        data['name']=user.name
        if not user:
            return Response({'error': 'User not found'}, status=404)

  
         
       
        del data['token']

        # data['image'] = image_base64
        # print(data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error_message = "Invalid input. Please check your details."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        

class Delete_feed(APIView):
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

        user = uu.objects.filter(userid=payload.get('gid')).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)
        
        
        user.delete()
        return Response({'message': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)




       
        




class Update_feed(APIView):
    def post(self, request):

        token = request.data.get('token')
        content=request.data.get('content')
        date_added=request.data.get('date_added')
     
        if not token:
            return Response({'error': 'Token is missing'}, status=400)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token is expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=401)

        user = uu.objects.filter(userid=payload.get('gid'),date_added=date_added).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)



        if content:
            user.content=content

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
       
        

