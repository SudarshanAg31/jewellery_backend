from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as http_status

from .models import DeviceActivation
from .serializers import AccessRequestSerializer, DeviceStatusSerializer
from django.http import HttpResponse

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


@api_view(['GET', 'HEAD'])
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

def welcome(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jewellery Backend</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #B8860B 0%, #8B6508 100%);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 40px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            }
            h1 { font-size: 32px; margin: 0 0 10px 0; }
            p { font-size: 16px; opacity: 0.9; margin: 5px 0; }
            .status {
                display: inline-block;
                margin-top: 20px;
                padding: 8px 20px;
                background: #4CAF50;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💎 Jewellery Backend</h1>
            <p>Device Activation Server</p>
            <p>Version 1.0</p>
            <div class="status">● LIVE</div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html, content_type='text/html')