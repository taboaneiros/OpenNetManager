
from rest_framework import serializers

from apps.devices.models import ClientModel, DeviceModel, EventModel, InterfaceModel, SnapshotModel


class DeviceSerializer(serializers.ModelSerializer):
    """Device serializer."""

    class Meta:
        model = DeviceModel
        fields = [
            "id",
            "hostname",
            "vendor",
            "model",
            "firmware",
            "serial",
            "management_ip",
            "status",
        ]


class ClientSerializer(serializers.ModelSerializer):
    """Client serializer."""

    device_hostname = serializers.CharField(source="device.hostname", read_only=True)

    class Meta:
        model = ClientModel
        fields = [
            "id",
            "device",
            "device_hostname",
            "mac",
            "ip",
            "hostname",
            "signal",
            "rx",
            "tx",
            "last_seen",
            "is_online",
        ]


class InterfaceSerializer(serializers.ModelSerializer):
    """Interface serializer."""

    device_hostname = serializers.CharField(source="device.hostname", read_only=True)

    class Meta:
        model = InterfaceModel
        fields = ["id", "device", "device_hostname", "name", "status", "speed"]


class EventSerializer(serializers.ModelSerializer):
    """Event serializer."""

    device_hostname = serializers.CharField(source="device.hostname", read_only=True)

    class Meta:
        model = EventModel
        fields = ["id", "device", "device_hostname", "severity", "message", "occurred_at"]


class SnapshotSerializer(serializers.ModelSerializer):
    """Snapshot serializer."""

    device_hostname = serializers.CharField(source="device.hostname", read_only=True)

    class Meta:
        model = SnapshotModel
        fields = ["id", "device", "device_hostname", "timestamp", "duration", "payload"]


class CollectRequestSerializer(serializers.Serializer):
    """Collection request serializer."""

    device_id = serializers.IntegerField(min_value=1)
