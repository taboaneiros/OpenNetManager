from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Device:
    """Domain device entity."""

    id: int | None = None
    hostname: str = ""
    management_ip: str = ""
    vendor: str = ""
    model: str = ""
    firmware: str = ""
    serial: str = ""
    status: str = "unknown"
    ssh_port: int = 22
    ssh_username: str = ""
    ssh_password: str = ""


@dataclass(slots=True)
class Client:
    """Domain client entity."""

    id: int | None = None
    device_id: int | None = None
    mac: str = ""
    ip: str = ""
    hostname: str = ""
    signal: int = 0
    rx: str = ""
    tx: str = ""
    is_online: bool = True
    last_seen: datetime | None = None


@dataclass(slots=True)
class Snapshot:
    """Domain snapshot entity."""

    id: int | None = None
    device_id: int | None = None
    timestamp: datetime | None = None
    duration: float = 0.0
    payload: dict = field(default_factory=dict)


@dataclass(slots=True)
class InterfaceData:
    """Parsed interface data."""

    name: str
    status: str
    speed: str


@dataclass(slots=True)
class ClientData:
    """Parsed client data."""

    mac: str
    ip: str
    hostname: str
    signal: int
    rx: str
    tx: str
    is_online: bool = True


@dataclass(slots=True)
class SystemData:
    """Parsed system data."""

    hostname: str
    serial: str
    firmware: str
    model: str
    uptime: str


@dataclass(slots=True)
class VersionData:
    """Parsed version data."""

    firmware: str
    build: str