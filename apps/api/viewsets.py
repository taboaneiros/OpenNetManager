
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.api.serializers import (
    ClientSerializer,
    CollectRequestSerializer,
    DeviceSerializer,
    EventSerializer,
    InterfaceSerializer,
    SnapshotSerializer,
)
from apps.devices.models import (
    ClientModel,
    DeviceModel,
    EventModel,
    InterfaceModel,
    SnapshotModel,
)
from core.services.collector import CollectorService


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only device endpoint."""

    queryset = DeviceModel.objects.all()
    serializer_class = DeviceSerializer


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only client endpoint."""

    queryset = ClientModel.objects.select_related("device").all()
    serializer_class = ClientSerializer


class InterfaceViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only interface endpoint."""

    queryset = InterfaceModel.objects.select_related("device").all()
    serializer_class = InterfaceSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only event endpoint."""

    queryset = EventModel.objects.select_related("device").all()
    serializer_class = EventSerializer


class SnapshotViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only snapshot endpoint."""

    queryset = SnapshotModel.objects.select_related("device").all()
    serializer_class = SnapshotSerializer


class SystemViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """System endpoint based on device data."""

    queryset = DeviceModel.objects.all()
    serializer_class = DeviceSerializer


class CollectViewSet(viewsets.ViewSet):
    """Collection trigger endpoint."""

    service_class = CollectorService

    def create(self, request):
        """Run a collection for a specific device."""
        serializer = CollectRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = self.service_class()
        snapshot = service.collect_device(serializer.validated_data["device_id"])
        return Response(snapshot, status=status.HTTP_201_CREATED)
