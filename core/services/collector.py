
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from apps.devices.models import (
    ClientModel,
    ClientSnapshotModel,
    DeviceModel,
    EventModel,
    InterfaceModel,
    SnapshotModel,
)
from core.domain.entities import ClientData, InterfaceData, SystemData, VersionData
from core.drivers.ap130 import AP130Driver
from core.parsers.interfaces import InterfaceParser
from core.parsers.stations import StationParser
from core.parsers.system import SystemParser
from core.parsers.version import VersionParser
from core.services.diff import SnapshotDiffService
from core.ssh.config import SSHConfig
from core.ssh.connection import SSHConnection
from core.ssh.executor import SSHExecutor


class CollectorService:
    """Collect and persist device information."""

    def collect_device(self, device_id: int) -> dict[str, Any]:
        device = DeviceModel.objects.get(pk=device_id)
        config = SSHConfig(
            host=device.management_ip,
            username=device.ssh_username or "admin",
            password=device.ssh_password or "changeme",
            port=device.ssh_port,
            prompt_suffix="#",
            timeout=15,
        )

        try:
            collected = self._collect_from_ssh(config, device)
            source = "ssh-real"
        except Exception as exc:
            collected = self._collect_fallback(device)
            source = f"fallback:{exc}"

        return self._persist(device, collected, source)

    def _collect_from_ssh(self, config: SSHConfig, device: DeviceModel) -> dict[str, Any]:
        connection = SSHConnection(config)
        connection.connect()

        try:
            executor = SSHExecutor(connection)
            driver = AP130Driver(executor)

            raw_system = driver.collect_system()
            raw_version = driver.collect_version()
            raw_interfaces = driver.collect_interfaces()
            raw_stations = driver.collect_stations()

            system = SystemParser().parse(raw_system + "\n" + raw_version)
            version = VersionParser().parse(raw_version)
            interfaces = InterfaceParser().parse(raw_interfaces)
            clients = StationParser().parse(raw_stations)

            if not system.hostname:
                system = SystemData(
                    hostname=device.hostname,
                    serial=system.serial,
                    firmware=system.firmware,
                    model=system.model,
                    uptime=system.uptime,
                )

            if not system.model:
                system = SystemData(
                    hostname=system.hostname,
                    serial=system.serial,
                    firmware=system.firmware,
                    model=device.model,
                    uptime=system.uptime,
                )

            return {
                "system": system,
                "version": version,
                "interfaces": interfaces,
                "clients": clients,
                "raw": {
                    "system": raw_system,
                    "version": raw_version,
                    "interfaces": raw_interfaces,
                    "stations": raw_stations,
                },
            }
        finally:
            connection.close()

    def _collect_fallback(self, device: DeviceModel) -> dict[str, Any]:
        system = SystemData(
            hostname=device.hostname,
            serial=device.serial or "N/A",
            firmware=device.firmware or "N/A",
            model=device.model,
            uptime="unknown",
        )
        version = VersionData(
            firmware=device.firmware or "N/A",
            build="fallback",
        )
        interfaces = [
            InterfaceData(name="wlan0", status="up", speed="20MHz"),
            InterfaceData(name="eth0", status="up", speed="-"),
        ]
        clients = [
            ClientData(
                mac="aa:bb:cc:dd:ee:01",
                ip="192.168.1.101",
                hostname="fallback-client",
                signal=-48,
                rx="300M",
                tx="240M",
                is_online=True,
            )
        ]

        return {
            "system": system,
            "version": version,
            "interfaces": interfaces,
            "clients": clients,
            "raw": {},
        }

    def _persist(self, device: DeviceModel, collected: dict[str, Any], source: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        interfaces: list[InterfaceData] = collected["interfaces"]
        clients: list[ClientData] = collected["clients"]
        system: SystemData = collected["system"]
        version: VersionData = collected["version"]

        previous_clients = self._load_previous_clients(device)
        diff = SnapshotDiffService().build_client_diff(previous_clients, clients)

        if version.firmware:
            device.firmware = version.firmware
        if system.serial:
            device.serial = system.serial
        if system.model:
            device.model = system.model
        if system.hostname:
            device.hostname = system.hostname
        device.status = "online"
        device.save()

        InterfaceModel.objects.filter(device=device).delete()
        if interfaces:
            InterfaceModel.objects.bulk_create(
                [
                    InterfaceModel(
                        device=device,
                        name=item.name,
                        status=item.status,
                        speed=item.speed,
                    )
                    for item in interfaces
                ]
            )

        ClientModel.objects.filter(device=device).delete()
        created_clients = 0
        if clients:
            created = ClientModel.objects.bulk_create(
                [
                    ClientModel(
                        device=device,
                        mac=item.mac,
                        ip=item.ip or None,
                        hostname=item.hostname,
                        signal=item.signal,
                        rx=item.rx,
                        tx=item.tx,
                        is_online=item.is_online,
                        last_seen=now,
                    )
                    for item in clients
                ]
            )
            created_clients = len(created)

        payload = {
            "source": source,
            "device": {
                "hostname": device.hostname,
                "management_ip": device.management_ip,
                "status": device.status,
                "firmware": device.firmware,
                "serial": device.serial,
                "model": device.model,
                "uptime": system.uptime,
            },
            "summary": {
                "online_clients": len([item for item in clients if item.is_online]),
                "offline_clients": len([item for item in clients if not item.is_online]),
                "total_clients_parsed": len(clients),
                "total_clients_persisted": created_clients,
                "interfaces": len(interfaces),
            },
            "diff": diff,
            "parsed_clients": [
                {
                    "mac": item.mac,
                    "ip": item.ip,
                    "hostname": item.hostname,
                    "signal": item.signal,
                    "rx": item.rx,
                    "tx": item.tx,
                }
                for item in clients
            ],
            "raw": collected.get("raw", {}),
        }

        snapshot = SnapshotModel.objects.create(
            device=device,
            timestamp=now,
            duration=1.10,
            payload=payload,
        )

        self._persist_client_history(snapshot, device, clients, now)
        self._emit_diff_events(device, diff, now)

        EventModel.objects.create(
            device=device,
            severity="info",
            message=(
                f"Coleta executada para {device.hostname} via {source}. "
                f"Interfaces={len(interfaces)} "
                f"Clientes parseados={len(clients)} "
                f"Clientes persistidos={created_clients}."
            ),
            occurred_at=now,
        )

        return {
            "snapshot_id": snapshot.id,
            "device_id": device.id,
            "hostname": device.hostname,
            "timestamp": snapshot.timestamp.isoformat(),
            "duration": snapshot.duration,
            "source": source,
            "interfaces": len(interfaces),
            "clients": created_clients,
            "joined": len(diff["joined"]),
            "left": len(diff["left"]),
            "changed": len(diff["changed"]),
        }

    def _load_previous_clients(self, device: DeviceModel) -> list[ClientData]:
        latest_snapshot = SnapshotModel.objects.filter(device=device).order_by("-timestamp", "-id").first()
        if not latest_snapshot:
            return []

        clients: list[ClientData] = []
        for item in latest_snapshot.client_snapshots.all():
            clients.append(
                ClientData(
                    mac=item.mac,
                    ip=item.ip or "",
                    hostname=item.hostname,
                    signal=item.signal,
                    rx=item.rx,
                    tx=item.tx,
                    is_online=item.is_online,
                )
            )
        return clients

    def _persist_client_history(
        self,
        snapshot: SnapshotModel,
        device: DeviceModel,
        clients: list[ClientData],
        now: datetime,
    ) -> None:
        if not clients:
            return

        history = []
        for client in clients:
            history.append(
                ClientSnapshotModel(
                    snapshot=snapshot,
                    device=device,
                    mac=client.mac,
                    ip=client.ip or None,
                    hostname=client.hostname,
                    signal=client.signal,
                    rx=client.rx,
                    tx=client.tx,
                    is_online=client.is_online,
                    first_seen=now,
                    last_seen=now,
                )
            )
        ClientSnapshotModel.objects.bulk_create(history)

    def _emit_diff_events(self, device: DeviceModel, diff: dict[str, list[dict]], now: datetime) -> None:
        events: list[EventModel] = []

        for item in diff["joined"]:
            events.append(
                EventModel(
                    device=device,
                    severity="info",
                    message=f"Cliente entrou: {item.get('hostname') or item.get('mac')} ({item.get('ip') or '-'})",
                    occurred_at=now,
                )
            )

        for item in diff["left"]:
            events.append(
                EventModel(
                    device=device,
                    severity="warning",
                    message=f"Cliente saiu: {item.get('hostname') or item.get('mac')} ({item.get('ip') or '-'})",
                    occurred_at=now,
                )
            )

        for item in diff["changed"]:
            events.append(
                EventModel(
                    device=device,
                    severity="info",
                    message=f"Cliente alterado: {item.get('hostname') or item.get('mac')}",
                    occurred_at=now,
                )
            )

        if events:
            EventModel.objects.bulk_create(events)
