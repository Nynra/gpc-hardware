from abc import ABC, abstractmethod


class AppCommandException(Exception):
    """Exception raised when a command for an app fails."""
    pass


class AppException(Exception):
    """Exception raised when an app fails."""
    pass


class BaseApp(ABC):
    """Base class for a GPC app."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the app."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the app."""
        pass

    @abstractmethod
    def start(self) -> ...:
        """Run the app."""
        pass

    @abstractmethod
    def stop(self) -> ...:
        """Stop the app."""
        pass

    @abstractmethod
    def emergency_stop(self) -> ...:
        """Emergency stop the app."""
        pass

    @abstractmethod
    def execute_command(self, cmd: str, *args, **kwargs) -> ...:
        """Execute a command."""
        pass