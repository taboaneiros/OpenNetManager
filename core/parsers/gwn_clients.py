from __future__ import annotations

import re

from core.domain.entities import ClientData


class GWNClientParser:
    """Parse GWN7600 client list output."""

    # Pattern for client lines:
    # [1] c283c0bf15a0  A56-de-Car Wireless  192.168.1.9  2.4G/11  104/78  Offline  000b82afe778 -67  Guieiro 2.4G
    #
    # Fields: [index] MAC Hostname Type IP Radio/Ch TX/RX Status AP_MAC RSSI SSID

    CLIENT_LINE_RE = re.compile(
        r"\[(\d+)\]\s+"                           # [1]
        r"([0-9a-f]{12})\s+"                      # MAC (sem dois pontos)
        r"(.+?)\s+"                               # Hostname (pode ter espaços)
        r"(Wireless|Wired)\s+"                    # Type
        r"(\d+\.\d+\.\d+\.\d+)\s+"                # IP Address
        r"(\S+)\s+"                               # Radio/Channel (e.g., 2.4G/11)
        r"(\d+/\d+)\s+"                           # TX/RX Rate
        r"(Online|Offline)\s+"                    # Status
        r"([0-9a-f]{12})\s+"                      # AP MAC
        r"(-?\d+)\s+"                             # RSSI
        r"(.+)"                                   # SSID (rest of line)
    )

    # Simpler fallback pattern for less strict matching
    SIMPLE_CLIENT_RE = re.compile(
        r"\[(\d+)\]\s+"
        r"([0-9a-f]{12})\s+"
    )

    # Header pattern to detect summary line
    SUMMARY_RE = re.compile(r"Total:\s*(\d+)\s+Online:\s*(\d+)")

    def parse(self, raw_text: str) -> list[ClientData]:
        """Parse client list from GWN7600 menu output."""
        clients: list[ClientData] = []

        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Skip header/summary lines
            if self._is_header_line(line):
                continue

            client = self._parse_client_line(line)
            if client:
                clients.append(client)

        return clients

    def _is_header_line(self, line: str) -> bool:
        """Check if line is a header or summary line."""
        skip_markers = [
            "GWN",
            "Clients (",
            "Mac",
            "Total:",
            "Online:",
            "[x] Back",
            "[z] Exit",
            "[r] Refresh",
            "Select by pressing",
            "Select a client",
        ]
        return any(marker in line for marker in skip_markers)

    def _parse_client_line(self, line: str) -> ClientData | None:
        """Parse a single client line."""
        match = self.CLIENT_LINE_RE.match(line)
        if not match:
            return None

        (
            index,
            mac_raw,
            hostname,
            client_type,
            ip,
            radio_channel,
            tx_rx,
            status,
            ap_mac,
            rssi,
            ssid,
        ) = match.groups()

        # Normalize MAC address (add colons)
        mac = self._normalize_mac(mac_raw)

        # Parse TX/RX rates
        tx, rx = self._parse_tx_rx(tx_rx)

        # Parse signal (RSSI)
        signal = int(rssi) if rssi else 0

        # Determine online status
        is_online = status.lower() == "online"

        # Clean hostname
        hostname = hostname.strip()

        return ClientData(
            mac=mac,
            ip=ip,
            hostname=hostname,
            signal=signal,
            rx=rx,
            tx=tx,
            is_online=is_online,
        )

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

    def _parse_tx_rx(self, tx_rx: str) -> tuple[str, str]:
        """Parse TX/RX rate string like '104/78'."""
        if "/" in tx_rx:
            parts = tx_rx.split("/")
            if len(parts) == 2:
                return f"{parts[0]}M", f"{parts[1]}M"
        return tx_rx, ""

    def parse_summary(self, raw_text: str) -> dict:
        """Parse summary information (Total/Online counts)."""
        total = 0
        online = 0

        for line in raw_text.splitlines():
            match = self.SUMMARY_RE.search(line)
            if match:
                total = int(match.group(1))
                online = int(match.group(2))
                break

        return {
            "total": total,
            "online": online,
            "offline": total - online,
        }