from __future__ import annotations

import json
import re

from core.domain.entities import ClientData


class StationParser:
    """Parse station output into client entities."""

    MAC_RE = re.compile(
        r"(?:"
        r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}"
        r"|"
        r"(?:[0-9A-Fa-f]{4}:){2}[0-9A-Fa-f]{4}"
        r")"
    )
    IPV4_RE = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")

    def parse(self, raw_text: str) -> list[ClientData]:
        """Parse clients from JSON, rt-sta, or generic table output."""
        text = raw_text.strip()
        if not text:
            return []

        json_clients = self._parse_json_payload(text)
        if json_clients:
            return json_clients

        rt_sta_clients = self._parse_rt_sta(text)
        if rt_sta_clients:
            return rt_sta_clients

        return self._parse_generic_table(text)

    def _parse_json_payload(self, text: str) -> list[ClientData]:
        """Parse one or more JSON objects from concatenated output."""
        clients = self._parse_json_with_raw_decode(text)
        if clients:
            return clients

        clients = self._parse_json_with_array_wrap(text)
        if clients:
            return clients

        return []

    def _parse_json_with_raw_decode(self, text: str) -> list[ClientData]:
        """Parse concatenated or comma-separated JSON objects incrementally."""
        decoder = json.JSONDecoder()
        index = 0
        length = len(text)
        clients: list[ClientData] = []

        while index < length:
            while index < length and text[index] in {" ", "\t", "\r", "\n", ","}:
                index += 1

            if index >= length:
                break

            if text[index] != "{":
                index += 1
                continue

            try:
                data, next_index = decoder.raw_decode(text, index)
            except json.JSONDecodeError:
                index += 1
                continue

            client = self._from_json_object(data)
            if client:
                clients.append(client)

            index = next_index

        return clients

    def _parse_json_with_array_wrap(self, text: str) -> list[ClientData]:
        """Fallback parser for strings like {...},{...} or {...}{...}."""
        normalized = text.strip()

        if not normalized:
            return []

        normalized = normalized.replace("}{", "},{")
        if not normalized.startswith("["):
            normalized = f"[{normalized}]"

        try:
            data = json.loads(normalized)
        except json.JSONDecodeError:
            return []

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            return []

        clients: list[ClientData] = []
        for item in data:
            client = self._from_json_object(item)
            if client:
                clients.append(client)
        return clients

    def _from_json_object(self, data: object) -> ClientData | None:
        """Convert one JSON object into ClientData."""
        if not isinstance(data, dict):
            return None

        mac = str(data.get("mac", "")).strip().lower()
        if not self.MAC_RE.fullmatch(mac):
            return None

        hostname = str(data.get("hostname", "")).strip() or mac.replace(":", "")
        ip = str(data.get("ip", "")).strip()
        tx = self._normalize_rate(data.get("txrate"))
        rx = self._normalize_rate(data.get("rxrate"))
        signal = self._normalize_signal(data.get("signal"))

        return ClientData(
            mac=mac,
            ip=ip,
            hostname=hostname,
            signal=signal,
            rx=rx,
            tx=tx,
            is_online=True,
        )

    def _parse_rt_sta(self, text: str) -> list[ClientData]:
        """Parse fallback rt-sta output."""
        clients: list[ClientData] = []

        for line in text.splitlines():
            row = line.strip()
            if not row:
                continue

            mac_match = self.MAC_RE.search(row)
            ip_match = self.IPV4_RE.search(row)
            if not mac_match or not ip_match:
                continue

            mac = mac_match.group(0).lower()
            ip = ip_match.group(0)
            middle = row[mac_match.end() : ip_match.start()].strip()
            hostname = re.sub(r"\s{2,}", " ", middle).strip() or mac.replace(":", "")

            clients.append(
                ClientData(
                    mac=mac,
                    ip=ip,
                    hostname=hostname,
                    signal=0,
                    rx="",
                    tx="",
                    is_online=True,
                )
            )

        return clients

    def _parse_generic_table(self, text: str) -> list[ClientData]:
        """Fallback parser for generic station tables."""
        clients: list[ClientData] = []

        for line in text.splitlines():
            row = line.strip()
            if not row:
                continue

            mac_match = self.MAC_RE.search(row)
            if not mac_match:
                continue

            mac = mac_match.group(0).lower()
            ip_match = self.IPV4_RE.search(row)
            ip = ip_match.group(0) if ip_match else ""

            rates = re.findall(r"\b\d+(?:\.\d+)?\s*[KMG]\b", row, re.IGNORECASE)
            tx = self._normalize_rate(rates[0]) if len(rates) > 0 else ""
            rx = self._normalize_rate(rates[1]) if len(rates) > 1 else ""
            signal = self._extract_signal(row)

            hostname = ""
            if ip:
                middle = row[mac_match.end() : ip_match.start()].strip()
                hostname = re.sub(r"\s{2,}", " ", middle).strip()
            hostname = hostname or mac.replace(":", "")

            clients.append(
                ClientData(
                    mac=mac,
                    ip=ip,
                    hostname=hostname,
                    signal=signal,
                    rx=rx,
                    tx=tx,
                    is_online=True,
                )
            )

        return clients

    def _extract_signal(self, text: str) -> int:
        """Extract signal from generic row."""
        match = re.search(r"(-?\d+)\((\d+)\)", text)
        if match:
            return int(match.group(1))

        match = re.search(r"-\d{1,3}", text)
        if match:
            return int(match.group(0))

        return 0

    def _normalize_rate(self, value: object) -> str:
        """Normalize transfer rate values."""
        if value is None:
            return ""
        text = str(value).strip()
        return (
            text.replace(" Mbps", "M")
            .replace(" mbps", "M")
            .replace(" Gbps", "G")
            .replace(" gbps", "G")
            .replace(" M", "M")
            .replace(" G", "G")
            .replace(" ", "")
        )

    def _normalize_signal(self, value: object) -> int:
        """Convert positive AP value to negative dBm-like value."""
        try:
            number = int(value)
        except (TypeError, ValueError):
            return 0
        return -abs(number)