from django.contrib import admin
from django.utils import timezone
from .models import DeviceActivation


@admin.register(DeviceActivation)
class DeviceActivationAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'short_device_id', 'status', 'requested_at', 'approved_at')
    list_filter = ('status', 'requested_at')
    search_fields = ('device_id', 'device_name')
    readonly_fields = ('device_id', 'requested_at', 'updated_at', 'activation_token')
    actions = ['approve_devices', 'reject_devices', 'block_devices']

    def short_device_id(self, obj):
        return f"{obj.device_id[:12]}..."
    short_device_id.short_description = 'Device ID'

    @admin.action(description='✅ Approve selected devices')
    def approve_devices(self, request, queryset):
        count = 0
        for device in queryset:
            if device.status in ['PENDING', 'REJECTED', 'BLOCKED']:
                device.status = 'APPROVED'
                device.approved_at = timezone.now()
                device.generate_token()
                device.save()
                count += 1
        self.message_user(request, f'{count} device(s) approved.')

    @admin.action(description='❌ Reject selected devices')
    def reject_devices(self, request, queryset):
        count = queryset.update(status='REJECTED', updated_at=timezone.now())
        self.message_user(request, f'{count} device(s) rejected.')

    @admin.action(description='🚫 Block selected devices')
    def block_devices(self, request, queryset):
        count = queryset.update(status='BLOCKED', updated_at=timezone.now())
        self.message_user(request, f'{count} device(s) blocked.')