from rest_framework import serializers
from .models import Message

class Messageserialiser(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['room', 'message', 'date_added']
