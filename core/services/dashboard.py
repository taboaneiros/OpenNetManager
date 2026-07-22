
from __future__ import annotations

from django.db.models import Count

from apps.devices.models import ClientModel, DeviceModel, EventModel, SnapshotModel


class DashboardMetricsService:
    """Build operational dashboard metrics."""

    def build_overview(self) -> dict:
        total_devices = DeviceModel.objects.count()
        online_devices = DeviceModel.objects.filter(status="online").count()
        offline_devices = DeviceModel.objects.filter(status="offline").count()
        total_clients = ClientModel.objects.filter(is_online=True).count()
        total_snapshots = SnapshotModel.objects.count()
        latest_events = EventModel.objects.select_related("device")[:10]

        busiest_devices = (
            DeviceModel.objects.annotate(client_count=Count("clients"))
            .order_by("-client_count", "hostname")[:5]
        )

        recent_snapshots = SnapshotModel.objects.select_related("device")[:10]

        return {
            "totals": {
                "devices": total_devices,
                "online_devices": online_devices,
                "offline_devices": offline_devices,
                "clients": total_clients,
                "snapshots": total_snapshots,
            },
            "latest_events": latest_events,
            "busiest_devices": busiest_devices,
            "recent_snapshots": recent_snapshots,
        }
