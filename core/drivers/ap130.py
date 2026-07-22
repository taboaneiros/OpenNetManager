from __future__ import annotations

import re
from types import SimpleNamespace

from core.drivers.base import BaseDriver


class AP130Driver(BaseDriver):
    """Driver for AP130 devices with compatibility helpers for tests."""

    SYSTEM_COMMANDS = (
        "show system",
        "show sysinfo",
    )
    VERSION_COMMANDS = (
        "show version",
        "show system version",
    )
    INTERFACE_COMMANDS = (
        "show interfaces",
        "show interface",
    )
    STATION_COMMANDS = (
        "show _client detail info",
    )

    def execute(self, command: str) -> str:
        """Execute a command using the underlying executor/connection."""
        if hasattr(self.executor, "execute"):
            return self.executor.execute(command)
        raise AttributeError("Executor does not provide execute().")

    def collect_system(self) -> str:
        return self._run_with_fallback(self.SYSTEM_COMMANDS)

    def collect_version(self) -> str:
        return self._run_with_fallback(self.VERSION_COMMANDS)

    def collect_interfaces(self) -> str:
        return self._run_with_fallback(self.INTERFACE_COMMANDS)

    def collect_stations(self) -> str:
        return self._run_with_fallback(self.STATION_COMMANDS)

    def collect_all(self) -> dict[str, str]:
        return {
            "system": self.collect_system(),
            "version": self.collect_version(),
            "interfaces": self.collect_interfaces(),
            "stations": self.collect_stations(),
        }

    def collect(self) -> dict[str, object]:
        """Compatibility collection method expected by legacy tests."""
        raw_version = self.execute("show version")
        raw_system = self.execute("show system")
        raw_stations = self.execute("show stations")
        raw_interfaces = self.execute("show interfaces")

        firmware = self._parse_firmware(raw_version)
        clients = self._parse_clients(raw_stations)
        interfaces = self._parse_interfaces(raw_interfaces)

        system = SimpleNamespace(firmware=firmware, raw=raw_system)

        return {
            "system": system,
            "clients": clients,
            "interfaces": interfaces,
            "raw": {
                "version": raw_version,
                "system": raw_system,
                "stations": raw_stations,
                "interfaces": raw_interfaces,
            },
        }

    def _run_with_fallback(self, commands: tuple[str, ...]) -> str:
        last_output = ""

        for command in commands:
            output = self.execute(command)
            last_output = output
            if self._is_valid_output(output):
                return output

        return last_output

    def _is_valid_output(self, output: str) -> bool:
        normalized = output.strip().lower()
        if not normalized:
            return False

        invalid_markers = (
            "unknown command",
            "invalid input",
            "incomplete command",
            "% error",
            "error:",
        )
        return not any(marker in normalized for marker in invalid_markers)

    def _parse_firmware(self, raw_version: str) -> str:
        match = re.search(r"firmware version:\s*(.+)", raw_version, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _parse_clients(self, raw_stations: str) -> list[SimpleNamespace]:
        lines = [line.strip() for line in raw_stations.splitlines() if line.strip()]
        if len(lines) < 2:
            return []

        clients: list[SimpleNamespace] = []
        for line in lines[1:]:
            parts = [part.strip() for part in line.split("|")]
            if len(parts) < 6:
                continue
            clients.append(
                SimpleNamespace(
                    mac=parts[0],
                    ip=parts[1],
                    hostname=parts[2],
                    signal=parts[3],
                    rx=parts[4],
                    tx=parts[5],
                )
            )
        return clients

    def _parse_interfaces(self, raw_interfaces: str) -> list[SimpleNamespace]:
        lines = [line.strip() for line in raw_interfaces.splitlines() if line.strip()]
        if len(lines) < 2:
            return []

        interfaces: list[SimpleNamespace] = []
        for line in lines[1:]:
            parts = [part.strip() for part in line.split("|")]
            if len(parts) < 3:
                continue
            interfaces.append(
                SimpleNamespace(
                    name=parts[0],
                    status=parts[1],
                    speed=parts[2],
                )
            )
        return interfaces