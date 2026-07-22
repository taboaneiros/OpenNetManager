from core.parsers.interfaces import InterfaceParser
from core.parsers.stations import StationParser
from core.parsers.system import SystemParser
from core.parsers.version import VersionParser


def test_station_parser_single_json_object():
    raw = (
        '{"mac":"2016:b966:eb53","username":"N/A","attribute":0,'
        '"bssid":"885b:dd02:cbe4","ip":"192.168.1.8",'
        '"hostname":"carlos-Aspire-F5-573G","ssid":"Guieiro-5G",'
        '"OS":"unknown","Domain":"","apname":"AH-02cbc0","channel":149,'
        '"txrate":"585 M","rxrate":"650 M","signal":31,"authmode":"WPA2-PSK",'
        '"encryption":"AES CCMP","vlan":1,"assmode":"11ac","asstime":"11:51:47",'
        '"txpacket":1329243,"txbytes":"2.94 GB","rxpacket":558331,'
        '"rxbytes":"141.18 MB"}'
    )

    clients = StationParser().parse(raw)

    assert len(clients) == 1
    assert clients[0].hostname == "carlos-Aspire-F5-573G"
    assert clients[0].ip == "192.168.1.8"


def test_station_parser_comma_separated_json_objects():
    raw = (
        '{"mac":"2016:b966:eb53","ip":"192.168.1.8","hostname":"carlos-Aspire-F5-573G",'
        '"txrate":"585 M","rxrate":"6 M","signal":35},'
        '{"mac":"1a27:6bc1:912b","ip":"192.168.1.20","hostname":"A56-de-Carlos",'
        '"txrate":"433.3 M","rxrate":"6 M","signal":30}'
    )

    clients = StationParser().parse(raw)

    assert len(clients) == 2
    assert clients[0].hostname == "carlos-Aspire-F5-573G"
    assert clients[1].hostname == "A56-de-Carlos"
    assert clients[1].ip == "192.168.1.20"


def test_station_parser_concatenated_json_objects():
    raw = (
        '{"mac":"2016:b966:eb53","ip":"192.168.1.8","hostname":"carlos-Aspire-F5-573G",'
        '"txrate":"585 M","rxrate":"6 M","signal":35}'
        '{"mac":"1a27:6bc1:912b","ip":"192.168.1.20","hostname":"A56-de-Carlos",'
        '"txrate":"433.3 M","rxrate":"6 M","signal":30}'
    )

    clients = StationParser().parse(raw)

    assert len(clients) == 2
    assert clients[0].hostname == "carlos-Aspire-F5-573G"
    assert clients[1].hostname == "A56-de-Carlos"


def test_station_parser_rt_sta():
    raw = (
        "2016:b966:eb53                                  "
        "carlos-Aspire-F5-573G            192.168.1.8      unknown(DHCP)"
    )

    clients = StationParser().parse(raw)

    assert len(clients) == 1
    assert clients[0].hostname == "carlos-Aspire-F5-573G"
    assert clients[0].ip == "192.168.1.8"


def test_interface_parser_ap130_rows():
    raw = (
        "Mgt0     885b:dd02:cbc0    -           U     -              1      -"
        "             hive0              -\n"
        "Wifi1.2  885b:dd02:cbe4 access         U    149*(80MHz)     -"
        "  WiFi5-AC          hive0          Guieiro-5G"
    )

    interfaces = InterfaceParser().parse(raw)

    assert len(interfaces) == 2
    assert interfaces[1].speed == "80MHz"


def test_system_parser_with_version_block():
    raw = (
        "Platform: AP130\n"
        "Uptime: 0 weeks, 6 days\n"
        "AP Name: AH-02cbc0"
    )

    system = SystemParser().parse(raw)

    assert system.model == "AP130"
    assert system.hostname == "AH-02cbc0"


def test_version_parser_hiveos():
    raw = (
        "Version: HiveOS 10.5r1 build-275676\n"
        "Build time: Thu Jul 28 02:59:41 UTC 2022\n"
        "Platform: AP130"
    )

    version = VersionParser().parse(raw)

    assert version.firmware == "HiveOS 10.5r1 build-275676"