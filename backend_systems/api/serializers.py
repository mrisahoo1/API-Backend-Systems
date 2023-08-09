from rest_framework import serializers
from .models import User, KeyValueData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class KeyValueDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyValueData
        fields = '__all__'
