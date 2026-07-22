
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.devices.models import (
    ClientModel,
    DeviceModel,
    EventModel,
    InterfaceModel,
    SnapshotModel,
)


class Command(BaseCommand):
    help = "Create local seed data for OpenNetManager."

    def handle(self, *args, **options) -> None:
        now = timezone.now()

        device, _ = DeviceModel.objects.get_or_create(
            management_ip="192.168.1.20",
            defaults={
                "hostname": "ap130-lab",
                "vendor": "AP130",
                "model": "AP130",
                "firmware": "2.1.0",
                "serial": "AP130-SERIAL-001",
                "status": "online",
                "ssh_username": "admin",
                "ssh_password": "changeme",
            },
        )

        InterfaceModel.objects.update_or_create(
            device=device,
            name="wlan0",
            defaults={"status": "up", "speed": "300M"},
        )
        InterfaceModel.objects.update_or_create(
            device=device,
            name="eth0",
            defaults={"status": "up", "speed": "1G"},
        )
        InterfaceModel.objects.update_or_create(
            device=device,
            name="bridge0",
            defaults={"status": "up", "speed": "1G"},
        )

        EventModel.objects.get_or_create(
            device=device,
            severity="info",
            message="Sistema iniciado com sucesso.",
            occurred_at=now - timedelta(hours=6),
        )
        EventModel.objects.get_or_create(
            device=device,
            severity="warning",
            message="Cliente com sinal fraco detectado.",
            occurred_at=now - timedelta(hours=2),
        )
        EventModel.objects.get_or_create(
            device=device,
            severity="info",
            message="Coleta de dados concluída.",
            occurred_at=now - timedelta(minutes=10),
        )

        ClientModel.objects.update_or_create(
            device=device,
            mac="AA:BB:CC:DD:EE:01",
            defaults={
                "ip": "192.168.1.101",
                "hostname": "notebook-ti",
                "signal": -48,
                "rx": "300M",
                "tx": "240M",
                "last_seen": now - timedelta(minutes=1),
                "is_online": True,
            },
        )
        ClientModel.objects.update_or_create(
            device=device,
            mac="AA:BB:CC:DD:EE:02",
            defaults={
                "ip": "192.168.1.102",
                "hostname": "smartphone-admin",
                "signal": -55,
                "rx": "144M",
                "tx": "120M",
                "last_seen": now - timedelta(minutes=3),
                "is_online": True,
            },
        )
        ClientModel.objects.update_or_create(
            device=device,
            mac="AA:BB:CC:DD:EE:03",
            defaults={
                "ip": "192.168.1.103",
                "hostname": "camera-hall",
                "signal": -72,
                "rx": "72M",
                "tx": "65M",
                "last_seen": now - timedelta(hours=5),
                "is_online": False,
            },
        )

        SnapshotModel.objects.create(
            device=device,
            timestamp=now - timedelta(minutes=30),
            duration=1.14,
            payload={
                "summary": {
                    "online_clients": 2,
                    "offline_clients": 1,
                    "total_clients": 3,
                }
            },
        )
        SnapshotModel.objects.create(
            device=device,
            timestamp=now,
            duration=1.24,
            payload={
                "system": {
                    "firmware": "2.1.0",
                    "serial": "AP130-SERIAL-001",
                    "cpu": "22%",
                    "memory": "47%",
                    "uptime": "8 days, 1 hour",
                },
                "summary": {
                    "online_clients": 2,
                    "offline_clients": 1,
                    "total_clients": 3,
                },
            },
        )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))
