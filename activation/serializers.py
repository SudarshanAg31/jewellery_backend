from rest_framework import serializers
from .models import DeviceActivation


class AccessRequestSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=128)
    device_name = serializers.CharField(max_length=255, required=False, allow_blank=True)


class DeviceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceActivation
        fields = ['device_id', 'device_name', 'status', 'activation_token',
                  'requested_at', 'approved_at', 'activated_at']