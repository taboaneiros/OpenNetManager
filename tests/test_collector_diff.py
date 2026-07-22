
import pytest

from apps.devices.models import ClientSnapshotModel, DeviceModel, SnapshotModel
from core.domain.entities import ClientData, InterfaceData, SystemData, VersionData
from core.services.collector import CollectorService


@pytest.mark.django_db
def test_collector_persist_creates_snapshot_history_and_diff():
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
    assert len(latest_snapshot.payload["diff"]["joined"]) == 1
    assert ClientSnapshotModel.objects.filter(snapshot=latest_snapshot).count() == 2
