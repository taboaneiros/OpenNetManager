
from core.domain.entities import ClientData
from core.services.diff import SnapshotDiffService


def test_build_client_diff_detects_join_left_and_change():
    previous = [
        ClientData(
            mac="2016:b966:eb53",
            ip="192.168.1.8",
            hostname="carlos-Aspire-F5-573G",
            signal=-30,
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
    ]
    current = [
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
            mac="9a96:db3c:c69d",
            ip="192.168.1.24",
            hostname="A54-de-Leila",
            signal=-26,
            rx="390M",
            tx="195M",
            is_online=True,
        ),
    ]

    diff = SnapshotDiffService().build_client_diff(previous, current)

    assert len(diff["joined"]) == 1
    assert diff["joined"][0]["hostname"] == "A54-de-Leila"
    assert len(diff["left"]) == 1
    assert diff["left"][0]["hostname"] == "A56-de-Carlos"
    assert len(diff["changed"]) == 1
    assert diff["changed"][0]["mac"] == "2016:b966:eb53"
    assert "signal" in diff["changed"][0]["changes"]
