import pytest

from apps.devices.models import ClientSnapshotModel, DeviceModel, EventModel, SnapshotModel
from core.domain.entities import ClientData, InterfaceData, SystemData, VersionData
from core.services.collector import CollectorService
from core.services.dashboard import DashboardMetricsService
from core.services.diff import SnapshotDiffService


@pytest.mark.django_db
def test_snapshot_diff_service_detects_join_leave_and_change():
    previous = [
        ClientData(
            mac="2016:b966:eb53",
            ip="192.168.1.8",
            hostname="carlos-Aspire-F5-573G",
            signal=-30,
            rx="650M",
            tx="6M",
            is_online=True,
        ),
        ClientData(
            mac="1a27:6bc1:912b",
            ip="192.168.1.20",
            hostname="A56-de-Carlos",
            signal=-37,
            rx="6M",
            tx="585M",
            is_online=True,
        ),
    ]
    current = [
        ClientData(
            mac="2016:b966:eb53",
            ip="192.168.1.8",
            hostname="carlos-Aspire-F5-573G",
            signal=-28,
            rx="650M",
            tx="6M",
            is_online=True,
        ),
        ClientData(
            mac="9a96:db3c:c69d",
            ip="192.168.1.24",
            hostname="A54-de-Leila",
            signal=-26,
            rx="390M",
            tx="195M",
            is_online=True,
        ),
    ]

    diff = SnapshotDiffService().build_client_diff(previous, current)

    assert len(diff["joined"]) == 1
    assert len(diff["left"]) == 1
    assert len(diff["changed"]) == 1
    assert diff["joined"][0]["hostname"] == "A54-de-Leila"
    assert diff["left"][0]["hostname"] == "A56-de-Carlos"
    assert diff["changed"][0]["mac"] == "2016:b966:eb53"


@pytest.mark.django_db
def test_dashboard_metrics_service_returns_expected_totals():
    device = DeviceModel.objects.create(
        hostname="AH-02cbc0",
        management_ip="192.168.1.2",
        status="online",
        vendor="Extreme Networks",
        model="AP130",
    )

    SnapshotModel.objects.create(
        device=device,
        timestamp="2026-07-19T01:00:00+00:00",
        duration=1.1,
        payload={"summary": {"online_clients": 1, "interfaces": 2}},
    )

    EventModel.objects.create(
        device=device,
        severity="info",
        message="Coleta executada com sucesso.",
        occurred_at="2026-07-19T01:00:00+00:00",
    )

    metrics = DashboardMetricsService().build_overview()

    assert metrics["totals"]["devices"] == 1
    assert metrics["totals"]["online_devices"] == 1
    assert metrics["totals"]["snapshots"] == 1
    assert len(metrics["latest_events"]) == 1


@pytest.mark.django_db
def test_collector_persist_creates_history_and_events():
    device = DeviceModel.objects.create(
        hostname="AH-02cbc0",
        management_ip="192.168.1.2",
        status="online",
        vendor="Extreme Networks",
        model="AP130",
    )

    previous_snapshot = SnapshotModel.objects.create(
        device=device,
        timestamp="2026-07-19T00:00:00+00:00",
        duration=1.0,
        payload={"summary": {"online_clients": 1}},
    )

    ClientSnapshotModel.objects.create(
        snapshot=previous_snapshot,
        device=device,
        mac="2016:b966:eb53",
        ip="192.168.1.8",
        hostname="carlos-Aspire-F5-573G",
        signal=-30,
        rx="650M",
        tx="6M",
        is_online=True,
    )

    service = CollectorService()
    result = service._persist(
        device=device,
        collected={
            "system": SystemData(
                hostname="AH-02cbc0",
                serial="SERIAL-001",
                firmware="HiveOS 10.5r1",
                model="AP130",
                uptime="1 day",
            ),
            "version": VersionData(
                firmware="HiveOS 10.5r1 build-275676",
                build="Thu Jul 28 02:59:41 UTC 2022",
            ),
            "interfaces": [
                InterfaceData(name="Wifi1.2", status="up", speed="80MHz"),
            ],
            "clients": [
                ClientData(
                    mac="2016:b966:eb53",
                    ip="192.168.1.8",
                    hostname="carlos-Aspire-F5-573G",
                    signal=-28,
                    rx="650M",
                    tx="6M",
                    is_online=True,
                ),
                ClientData(
                    mac="1a27:6bc1:912b",
                    ip="192.168.1.20",
                    hostname="A56-de-Carlos",
                    signal=-37,
                    rx="6M",
                    tx="585M",
                    is_online=True,
                ),
            ],
            "raw": {
                "system": "system",
                "version": "version",
                "interfaces": "interfaces",
                "stations": "stations",
            },
        },
        source="ssh-real",
    )

    latest_snapshot = SnapshotModel.objects.order_by("-timestamp", "-id").first()

    assert result["clients"] == 2
    assert result["joined"] == 1
    assert result["changed"] == 1
    assert latest_snapshot is not None
    assert latest_snapshot.payload["summary"]["online_clients"] == 2
    assert ClientSnapshotModel.objects.filter(snapshot=latest_snapshot).count() == 2
    assert EventModel.objects.filter(device=device).count() >= 1