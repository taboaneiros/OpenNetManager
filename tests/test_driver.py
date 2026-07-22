from types import SimpleNamespace
from unittest.mock import Mock

from core.drivers.ap130 import AP130Driver


def test_ap130_driver_collects_data(monkeypatch):
    connection = Mock()
    connection.config = SimpleNamespace(prompt="#", pagination_token="--More--")

    driver = AP130Driver(connection)

    outputs = {
        "show version": "Firmware Version: 2.0.0",
        "show system": "Serial: ABC\nCPU: 20%\nMemory: 40%\nUptime: 2 days",
        "show stations": "MAC | IP | Hostname | Signal | RX | TX\nAA | 10.0.0.2 | cli | -60 | 100M | 80M",
        "show interfaces": "Name | Status | Speed\neth0 | up | 1G",
    }
    monkeypatch.setattr(driver, "execute", lambda cmd: outputs[cmd])

    result = driver.collect()
    assert result["system"].firmware == "2.0.0"
    assert len(result["clients"]) == 1
    assert len(result["interfaces"]) == 1