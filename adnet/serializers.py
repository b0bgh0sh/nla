from rest_framework import serializers
from adnet.models import User, Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'user', 'advisor', 'time')
