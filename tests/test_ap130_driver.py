
from core.drivers.ap130 import AP130Driver


class FakeExecutor:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def execute(self, command: str) -> str:
        self.calls.append(command)
        return self.responses.get(command, "unknown command")


def test_ap130_driver_fallback_commands():
    responses = {
        "show system": "unknown command",
        "show sysinfo": "hostname: ap130-lab",
    }
    executor = FakeExecutor(responses)
    driver = AP130Driver(executor)

    output = driver.collect_system()

    assert output == "hostname: ap130-lab"
    assert executor.calls[:2] == ["show system", "show sysinfo"]
