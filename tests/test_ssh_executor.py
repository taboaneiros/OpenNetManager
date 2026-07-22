
from core.ssh.config import SSHConfig
from core.ssh.executor import SSHExecutor


class FakeShell:
    def __init__(self, responses):
        self.responses = responses
        self.sent = []
        self.index = 0

    def send(self, command):
        self.sent.append(command)

    def recv_ready(self):
        return self.index < len(self.responses)

    def recv(self, size):
        value = self.responses[self.index]
        self.index += 1
        return value.encode("utf-8")


class FakeConnection:
    def __init__(self, shell):
        self._shell = shell
        self.config = SSHConfig(
            host="192.168.1.20",
            username="admin",
            password="changeme",
        )

    @property
    def shell(self):
        return self._shell

    def close(self):
        return None

    def connect(self):
        return None


def test_executor_handles_more_prompt():
    shell = FakeShell(["show interfaces\nline 1\n--More--", "line 2\n#",])
    connection = FakeConnection(shell)
    executor = SSHExecutor(connection)

    output = executor.execute("show interfaces")

    assert "line 1" in output
    assert "line 2" in output
    assert "show interfaces\n" in shell.sent
    assert " " in shell.sent
