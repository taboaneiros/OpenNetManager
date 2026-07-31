"""Tests for GWN7600 parsers."""

import pytest

from core.parsers.gwn_system import GWNSystemParser
from core.parsers.gwn_clients import GWNClientParser
from core.parsers.gwn_radio import GWNRadioParser


class TestGWNSystemParser:
    """Tests for GWNSystemParser."""

    @pytest.fixture
    def parser(self) -> GWNSystemParser:
        return GWNSystemParser()

    def test_parse_status_output(self, parser: GWNSystemParser) -> None:
        """Test parsing complete status output."""
        raw = """
GWN7600(Master) - Wed Jul 29 22:10:47 -03 2026

GWN7600 Status

           Model: GWN7600
            Role: Master
             MAC: 000b82afe778
     Part Number: 9640000713B
    Boot Version: 0.0.0.2
Firmware Version: 1.0.25.33
          Uptime: 1:12:16:00


NET/POE - connected                      Uptime: 1:12:13:37


NET - disconnected                       Uptime: 0:00:00:00









[x] Back



Select by pressing the [number] or [letter] and then ENTER
"""
        result = parser.parse(raw)

        assert result.hostname == "GWN7600(Master)"
        assert result.model == "GWN7600"
        assert result.serial == "00:0b:82:af:e7:78"
        assert result.firmware == "1.0.25.33"
        assert result.uptime == "1:12:16:00"

    def test_parse_version(self, parser: GWNSystemParser) -> None:
        """Test parsing version information."""
        raw = """
Firmware Version: 1.0.25.33
Boot Version: 0.0.0.2
"""
        result = parser.parse_version(raw)

        assert result.firmware == "1.0.25.33"
        assert result.build == "0.0.0.2"

    def test_normalize_mac(self, parser: GWNSystemParser) -> None:
        """Test MAC address normalization."""
        assert parser._normalize_mac("000b82afe778") == "00:0b:82:af:e7:78"
        assert parser._normalize_mac("00:0b:82:af:e7:78") == "00:0b:82:af:e7:78"
        assert parser._normalize_mac("00-0B-82-AF-E7-78") == "00:0b:82:af:e7:78"
        assert parser._normalize_mac("") == ""

    def test_parse_network_interfaces(self, parser: GWNSystemParser) -> None:
        """Test parsing network interface status."""
        raw = """
NET/POE - connected                      Uptime: 1:12:13:37
NET - disconnected                       Uptime: 0:00:00:00
"""
        result = parser.parse_network_interfaces(raw)

        assert len(result) == 2
        assert result[0]["name"] == "NET/POE"
        assert result[0]["status"] == "connected"
        assert result[1]["name"] == "NET"
        assert result[1]["status"] == "disconnected"


class TestGWNClientParser:
    """Tests for GWNClientParser."""

    @pytest.fixture
    def parser(self) -> GWNClientParser:
        return GWNClientParser()

    def test_parse_client_line(self, parser: GWNClientParser) -> None:
        """Test parsing a single client line."""
        raw = """
[1] c283c0bf15a0  A56-de-Car Wireless  192.168.1.9  2.4G/11  104/78  Offline  000b82afe778 -67  Guieiro 2.4G
"""
        result = parser.parse(raw)

        assert len(result) == 1
        client = result[0]
        assert client.mac == "c2:83:c0:bf:15:a0"
        assert client.ip == "192.168.1.9"
        assert client.hostname == "A56-de-Car"
        assert client.signal == -67
        assert client.tx == "104M"
        assert client.rx == "78M"
        assert client.is_online is False

    def test_parse_multiple_clients(self, parser: GWNClientParser) -> None:
        """Test parsing multiple client lines."""
        raw = """
[1] c283c0bf15a0  Client1 Wireless  192.168.1.9  2.4G/11  104/78  Online  000b82afe778 -67  SSID1
[2] aabbccddeeff  Client2 Wireless  192.168.1.10  5G/36  300/300  Online  000b82afe778 -45  SSID5G
"""
        result = parser.parse(raw)

        assert len(result) == 2
        assert result[0].mac == "c2:83:c0:bf:15:a0"
        assert result[0].is_online is True
        assert result[1].mac == "aa:bb:cc:dd:ee:ff"
        assert result[1].signal == -45

    def test_skip_header_lines(self, parser: GWNClientParser) -> None:
        """Test that header lines are skipped."""
        raw = """
GWN7600(Master) - Wed Jul 29 22:20:02 -03 2026

Clients (Total: 2 Online: 2)

[1] c283c0bf15a0  Client1 Wireless  192.168.1.9  2.4G/11  104/78  Online  000b82afe778 -67  SSID

[x] Back
[z] Exit List
[r] Refresh

Select by pressing the [number] or [letter] and then ENTER
"""
        result = parser.parse(raw)

        assert len(result) == 1
        assert result[0].mac == "c2:83:c0:bf:15:a0"

    def test_parse_summary(self, parser: GWNClientParser) -> None:
        """Test parsing summary information."""
        raw = "Total: 15 Online: 12"
        result = parser.parse_summary(raw)

        assert result["total"] == 15
        assert result["online"] == 12
        assert result["offline"] == 3


class TestGWNRadioParser:
    """Tests for GWNRadioParser."""

    @pytest.fixture
    def parser(self) -> GWNRadioParser:
        return GWNRadioParser()

    def test_parse_radio_config(self, parser: GWNRadioParser) -> None:
        """Test parsing radio configuration."""
        raw = """
GWN7600(Master) - Wed Jul 29 22:20:02 -03 2026

Radio Configuration (:)

[1] Band Steering: Disabled

    
    
[3] Airtime Fairness: Disabled
[4] Beacon Interval (ms): 100
[5] 2g4   Channel Width: 40MHz       Short Guard Interval: Enabled                                 
         Channel: Auto            auto                                
         Radio Power: Medium                                 
         Allow Legacy Devices(802.11b): Disabled                                 
         Minimum RSSI: Enabled (-67dBm)                                 
         Minimum Access Rate Limit: Enabled (24Mbps)                                 
[6] 5g  Channel Width: 80MHz       Short Guard Interval: Enabled                                 
         Channel: Auto                                      
         Radio Power: Dynamically-Assigned-by-RRM                                 
         Minimum RSSI: Enabled (-75dBm)                                 
         Minimum Access Rate Limit: Disabled                                 









[x] Back


Edit an option
Select by pressing the [number] or [letter] and then ENTER
"""
        result = parser.parse(raw)

        assert len(result) == 2
        # 2g4 radio
        assert result[0].name == "wlan-2g4"
        assert result[0].status == "up"
        assert "40MHz" in result[0].speed
        assert "Medium" in result[0].speed
        # 5g radio
        assert result[1].name == "wlan-5g"
        assert result[1].status == "up"
        assert "80MHz" in result[1].speed
        assert "Dynamically-Assigned-by-RRM" in result[1].speed

    def test_parse_band_info(self, parser: GWNRadioParser) -> None:
        """Test parsing band information."""
        raw = """
[5] 2g4   Channel Width: 40MHz       Channel: Auto
[6] 5g  Channel Width: 80MHz       Channel: Auto
"""
        result = parser.parse_band_info(raw)

        assert "2g4" in result
        assert "5g" in result
        assert result["2g4"]["channel_width"] == "40MHz"
        assert result["5g"]["channel_width"] == "80MHz"