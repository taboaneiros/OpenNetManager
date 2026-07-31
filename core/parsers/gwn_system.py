from __future__ import annotations

import re

from core.domain.entities import SystemData, VersionData


class GWNSystemParser:
    """Parse GWN7600 status menu output."""

    MODEL_RE = re.compile(r"Model:\s*(\S+)")
    ROLE_RE = re.compile(r"Role:\s*(\S+)")
    MAC_RE = re.compile(r"MAC:\s*([0-9A-Fa-f]+)", re.IGNORECASE)
    FIRMWARE_RE = re.compile(r"Firmware Version:\s*([\d.]+)")
    BOOT_VERSION_RE = re.compile(r"Boot Version:\s*([\d.]+)")
    UPTIME_RE = re.compile(r"Uptime:\s*(\d+:\d+:\d+:\d+)")
    PART_NUMBER_RE = re.compile(r"Part Number:\s*(\S+)")

    def parse(self, raw_text: str) -> SystemData:
        """Parse system information from status menu output."""
        text = raw_text.strip()

        model = self._extract_field(text, self.MODEL_RE, "GWN7600")
        serial = self._normalize_mac(self._extract_field(text, self.MAC_RE, ""))
        firmware = self._extract_field(text, self.FIRMWARE_RE, "")
        uptime = self._extract_field(text, self.UPTIME_RE, "unknown")

        # Hostname is typically derived from model and role
        role = self._extract_field(text, self.ROLE_RE, "")
        hostname = f"{model}({role})" if role else model

        return SystemData(
            hostname=hostname,
            serial=serial,
            firmware=firmware,
            model=model,
            uptime=uptime,
        )

    def parse_version(self, raw_text: str) -> VersionData:
        """Parse version information from status menu output."""
        text = raw_text.strip()

        firmware = self._extract_field(text, self.FIRMWARE_RE, "")
        boot_version = self._extract_field(text, self.BOOT_VERSION_RE, "")

        return VersionData(
            firmware=firmware,
            build=boot_version,
        )

    def _extract_field(self, text: str, pattern: re.Pattern, default: str) -> str:
        """Extract a field using regex pattern."""
        match = pattern.search(text)
        return match.group(1).strip() if match else default

    def _normalize_mac(self, mac: str) -> str:
        """Normalize MAC address to standard format with colons."""
        if not mac:
            return ""

        # Remove any existing separators
        clean = mac.replace(":", "").replace("-", "").replace(".", "")

        # Add colons every 2 characters
        if len(clean) == 12:
            return ":".join(clean[i : i + 2] for i in range(0, 12, 2)).lower()

        return mac.lower()

    def parse_network_interfaces(self, raw_text: str) -> list[dict]:
        """Parse network interface status from status output."""
        interfaces: list[dict] = []

        # Pattern for interface lines like:
        # NET/POE - connected                      Uptime: 1:12:13:37
        # NET - disconnected                       Uptime: 0:00:00:00
        iface_pattern = re.compile(
            r"(NET(?:/POE)?)\s*-\s*(connected|disconnected)"
        )

        for line in raw_text.splitlines():
            match = iface_pattern.search(line)
            if match:
                interfaces.append(
                    {
                        "name": match.group(1),
                        "status": match.group(2),
                    }
                )

        return interfaces