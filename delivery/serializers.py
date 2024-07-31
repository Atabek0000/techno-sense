from rest_framework import serializers
from .models import DeliveryRequest


class DeliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryRequest
        fields = ['latitude_a', 'longitude_a', 'latitude_b', 'longitude_b']
