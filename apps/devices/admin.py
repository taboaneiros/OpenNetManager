from django.contrib import admin

from apps.devices.models import (
    ClientModel,
    ClientSnapshotModel,
    DeviceModel,
    EventModel,
    InterfaceModel,
    SnapshotModel,
)

admin.site.site_header = "OpenNetManager Admin"
admin.site.site_title = "OpenNetManager"
admin.site.index_title = "Administração da plataforma"


@admin.register(DeviceModel)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("hostname", "management_ip", "vendor", "model", "status", "firmware")
    search_fields = ("hostname", "management_ip", "model", "firmware")
    list_filter = ("status", "vendor", "model")


@admin.register(InterfaceModel)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ("device", "name", "status", "speed", "updated_at")
    search_fields = ("device__hostname", "name")
    list_filter = ("status",)


@admin.register(ClientModel)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("device", "hostname", "mac", "ip", "signal", "is_online", "last_seen")
    search_fields = ("device__hostname", "hostname", "mac", "ip")
    list_filter = ("is_online",)


@admin.register(SnapshotModel)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ("device", "timestamp", "duration")
    search_fields = ("device__hostname",)
    list_filter = ("device",)


@admin.register(ClientSnapshotModel)
class ClientSnapshotAdmin(admin.ModelAdmin):
    list_display = ("device", "hostname", "mac", "ip", "signal", "is_online", "last_seen")
    search_fields = ("device__hostname", "hostname", "mac", "ip")
    list_filter = ("is_online",)


@admin.register(EventModel)
class EventAdmin(admin.ModelAdmin):
    list_display = ("device", "severity", "occurred_at", "message")
    search_fields = ("device__hostname", "message")
    list_filter = ("severity",)