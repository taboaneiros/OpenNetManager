
import pytest

from apps.devices.models import ClientModel, DeviceModel, EventModel, SnapshotModel
from core.services.dashboard import DashboardMetricsService


@pytest.mark.django_db
def test_dashboard_metrics_service_builds_overview():
    device = DeviceModel.objects.create(
        hostname="AH-02cbc0",
        management_ip="192.168.1.2",
        status="online",
        vendor="Extreme Networks",
        model="AP130",
    )

    ClientModel.objects.create(
        device=device,
        mac="2016:b966:eb53",
        ip="192.168.1.8",
        hostname="carlos-Aspire-F5-573G",
        signal=-30,
        rx="650M",
        tx="6M",
        is_online=True,
    )

    SnapshotModel.objects.create(
        device=device,
        timestamp="2026-07-19T01:00:00+00:00",
        duration=1.1,
        payload={"summary": {"online_clients": 1, "interfaces": 7}},
    )

    EventModel.objects.create(
        device=device,
        severity="info",
        message="Cliente entrou: carlos-Aspire-F5-573G",
        occurred_at="2026-07-19T01:00:00+00:00",
    )

    data = DashboardMetricsService().build_overview()

    assert data["totals"]["devices"] == 1
    assert data["totals"]["online_devices"] == 1
    assert data["totals"]["clients"] == 1
    assert data["totals"]["snapshots"] == 1
    assert len(data["latest_events"]) == 1
    assert len(data["busiest_devices"]) == 1
