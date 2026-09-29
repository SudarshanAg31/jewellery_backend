from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as http_status

from .models import DeviceActivation
from .serializers import AccessRequestSerializer, DeviceStatusSerializer


@api_view(['POST'])
def request_access(request):
    serializer = AccessRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=http_status.HTTP_400_BAD_REQUEST)

    device_id = serializer.validated_data['device_id']
    device_name = serializer.validated_data.get('device_name', '')

    device, created = DeviceActivation.objects.get_or_create(
        device_id=device_id,
        defaults={'device_name': device_name, 'status': 'PENDING'}
    )

    if not created and device_name and device.device_name != device_name:
        device.device_name = device_name
        device.save()

    return Response({
        'request_id': str(device.id),
        'device_id': device.device_id,
        'status': device.status,
        'message': 'Access request received. Please wait for admin approval.',
    }, status=http_status.HTTP_200_OK)


@api_view(['GET'])
def check_status(request):
    device_id = request.query_params.get('device_id')
    if not device_id:
        return Response({'error': 'device_id required'}, status=http_status.HTTP_400_BAD_REQUEST)

    try:
        device = DeviceActivation.objects.get(device_id=device_id)
    except DeviceActivation.DoesNotExist:
        return Response({'error': 'Device not found'}, status=http_status.HTTP_404_NOT_FOUND)

    return Response(DeviceStatusSerializer(device).data, status=http_status.HTTP_200_OK)


@api_view(['POST'])
def mark_activated(request):
    device_id = request.data.get('device_id')
    if not device_id:
        return Response({'error': 'device_id required'}, status=http_status.HTTP_400_BAD_REQUEST)

    try:
        device = DeviceActivation.objects.get(device_id=device_id)
    except DeviceActivation.DoesNotExist:
        return Response({'error': 'Device not found'}, status=http_status.HTTP_404_NOT_FOUND)

    if device.status == 'APPROVED':
        device.status = 'ACTIVE'
        device.activated_at = timezone.now()
        device.save()

    return Response({'status': device.status}, status=http_status.HTTP_200_OK)