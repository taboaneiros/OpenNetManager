"""Tests for GWN7600 driver."""

import pytest
from unittest.mock import MagicMock, patch

from core.drivers.gwn7600 import GWN7600Driver
from core.ssh.menu_executor import GWNMenuExecutor


class TestGWN7600Driver:
    """Tests for GWN7600Driver."""

    @pytest.fixture
    def mock_executor(self) -> GWNMenuExecutor:
        """Create a mock menu executor."""
        executor = MagicMock(spec=GWNMenuExecutor)
        executor.navigate_to = MagicMock(return_value="mock output")
        executor.go_back = MagicMock(return_value="main menu")
        return executor

    @pytest.fixture
    def driver(self, mock_executor: GWNMenuExecutor) -> GWN7600Driver:
        """Create a GWN7600 driver with mock executor."""
        return GWN7600Driver(mock_executor)

    def test_collect_system(self, driver: GWN7600Driver, mock_executor: GWNMenuExecutor) -> None:
        """Test collecting system information."""
        result = driver.collect_system()

        mock_executor.navigate_to.assert_called_with("1")
        assert result == "mock output"

    def test_collect_stations(self, driver: GWN7600Driver, mock_executor: GWNMenuExecutor) -> None:
        """Test collecting connected clients."""
        result = driver.collect_stations()

        mock_executor.navigate_to.assert_called_with("4")
        assert result == "mock output"

    def test_collect_interfaces(self, driver: GWN7600Driver, mock_executor: GWNMenuExecutor) -> None:
        """Test collecting radio configuration."""
        result = driver.collect_interfaces()

        mock_executor.navigate_to.assert_called_with("10")
        assert result == "mock output"

    def test_collect_version(self, driver: GWN7600Driver, mock_executor: GWNMenuExecutor) -> None:
        """Test collecting version (same as system for GWN)."""
        result = driver.collect_version()

        # Version is same as system for GWN devices
        mock_executor.navigate_to.assert_called_with("1")
        assert result == "mock output"

    def test_collect_all(self, driver: GWN7600Driver, mock_executor: GWNMenuExecutor) -> None:
        """Test collecting all data."""
        mock_executor.navigate_to.side_effect = [
            "system output",
            "version output",
            "interfaces output",
            "stations output",
        ]

        result = driver.collect_all()

        assert result["system"] == "system output"
        assert result["version"] == "version output"
        assert result["interfaces"] == "interfaces output"
        assert result["stations"] == "stations output"

    def test_go_back(self, driver: GWN7600Driver, mock_executor: GWNMenuExecutor) -> None:
        """Test going back to previous menu."""
        result = driver.go_back()

        mock_executor.go_back.assert_called_once()
        assert result == "main menu"

    def test_execute_command(self, driver: GWN7600Driver, mock_executor: GWNMenuExecutor) -> None:
        """Test execute method (compatibility with BaseDriver)."""
        result = driver.execute("5")

        mock_executor.navigate_to.assert_called_with("5")
        assert result == "mock output"

    def test_menu_constants(self) -> None:
        """Test that menu constants are correct."""
        assert GWN7600Driver.MENU_STATUS == "1"
        assert GWN7600Driver.MENU_CLIENTS == "4"
        assert GWN7600Driver.MENU_RADIO == "10"


class TestGWNMenuExecutor:
    """Tests for GWNMenuExecutor."""

    @pytest.fixture
    def mock_connection(self) -> MagicMock:
        """Create a mock SSH connection."""
        connection = MagicMock()
        connection.shell = MagicMock()
        connection.shell.send = MagicMock()
        connection.shell.recv_ready = MagicMock(return_value=True)
        connection.shell.recv = MagicMock(
            return_value=b"GWN7600(Master)\n[x] Back\nSelect by pressing"
        )
        return connection

    def test_navigate_to_sends_option(self, mock_connection: MagicMock) -> None:
        """Test that navigate_to sends the correct menu option."""
        executor = GWNMenuExecutor(mock_connection)
        executor.navigate_to("4")

        # Should have sent "4\n"
        mock_connection.shell.send.assert_called()

    def test_go_back_sends_x(self, mock_connection: MagicMock) -> None:
        """Test that go_back sends 'x'."""
        executor = GWNMenuExecutor(mock_connection)
        executor.go_back()

        # Should have sent "x\n"
        calls = mock_connection.shell.send.call_args_list
        assert any("x" in str(call) for call in calls)

    def test_is_menu_complete(self, mock_connection: MagicMock) -> None:
        """Test detection of menu completion."""
        executor = GWNMenuExecutor(mock_connection)

        assert executor._is_menu_complete("[x] Back") is True
        assert executor._is_menu_complete("Select by pressing") is True
        assert executor._is_menu_complete("[z] Exit List") is True
        assert executor._is_menu_complete("Some random text") is False

    def test_clean_output_removes_ansi(self, mock_connection: MagicMock) -> None:
        """Test that ANSI escape sequences are removed."""
        executor = GWNMenuExecutor(mock_connection)

        # ANSI escape sequence
        dirty = "\x1b[32mGreen Text\x1b[0m"
        clean = executor._clean_output(dirty)

        assert "\x1b" not in clean
        assert "Green Text" in clean

    def test_clean_output_removes_carriage_returns(self, mock_connection: MagicMock) -> None:
        """Test that carriage returns are removed."""
        executor = GWNMenuExecutor(mock_connection)

        dirty = "line1\r\nline2\r\n"
        clean = executor._clean_output(dirty)

        assert "\r" not in clean