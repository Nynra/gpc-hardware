"""This module contains some base classes used in the daqc1 and 2 modules.

To make sure both modules are compatible, the base classes are defined here.
"""
from abc import ABC, abstractmethod


class BaseDigitalInput(ABC):
    """Base class for a digital input pin."""

    @property
    @abstractmethod
    def pin(self) -> int:
        """The pin number of the digital input pin."""
        pass
    
    @property
    @abstractmethod
    def state(self) -> int:
        """The value read from the digital input pin."""
        pass

    @abstractmethod
    def read(self) -> bool:
        """Read the digital input pin."""
        pass


class BaseDigitalOutput(ABC):
    """Base class for a digital output pin."""

    @property
    @abstractmethod
    def pin(self) -> int:
        """The pin number of the digital output pin."""
        pass

    @property
    @abstractmethod
    def state(self) -> int:
        """Get or set the state of the digital output pin."""
        pass

    @state.setter
    @abstractmethod
    def state(self, value: int) -> ...:
        pass

    @abstractmethod
    def write(self, value: int) -> ...:
        """Write a value to the digital output pin."""
        pass


class BaseAnalogInput(ABC):
    """Base class for an analog input pin."""

    @property
    @abstractmethod
    def pin(self) -> int:
        """The pin number of the analog input pin."""
        pass

    @property
    @abstractmethod
    def value(self) -> float:
        """The value read from the analog input pin."""
        pass

    @abstractmethod
    def read(self) -> float:
        """Read the analog input pin."""
        pass


class BaseAnalogOutput(ABC):
    """Base class for an analog output pin."""

    @property
    @abstractmethod
    def pin(self) -> int:
        """The pin number of the analog output pin."""
        pass

    @property
    @abstractmethod
    def value(self) -> float:
        """Get or set the value of the analog output pin."""
        pass

    @value.setter
    @abstractmethod
    def value(self, value: float) -> ...:
        pass

    @abstractmethod
    def write(self, value: float) -> ...:
        """Write a value to the analog output pin."""
        pass


# class BaseDigitalInterrupt(BaseDigitalInput):
#     """Base class for a digital input pin with interrupt capabilities."""

#     @property
#     @abstractmethod
#     def callback(self) -> Union[callable, None]:
#         """The callback function to be called when the interrupt is triggered."""
#         pass

#     @property
#     @abstractmethod
#     def interrupt_enabled(self) -> bool:
#         """Whether the interrupt is enabled."""
#         pass

#     @abstractmethod
#     def enable_interrupt(self, callback: callable) -> ...:
#         """Enable an interrupt on the digital input pin."""
#         pass

#     @abstractmethod
#     def disable_interrupt(self) -> ...:
#         """Disable the interrupt on the digital input pin."""
#         pass


class BasePlate(ABC):
    """Base class for a plate."""

    @property
    @abstractmethod
    def address(self) -> int:
        """The address of the plate."""
        pass

    @property
    @abstractmethod
    def firmware_version(self) -> str:
        """The firmware version of the plate."""
        pass

    @property
    @abstractmethod
    def hardware_version(self) -> str:
        """The hardware version of the plate."""
        pass

    @abstractmethod
    def get_digital_input(self, pin: int) -> BaseDigitalInput:
        """Get a digital input pin."""
        pass

    @abstractmethod
    def get_digital_output(self, pin: int) -> BaseDigitalOutput:
        """Get a digital output pin."""
        pass

    @abstractmethod
    def get_analog_input(self, pin: int) -> BaseAnalogInput:
        """Get an analog input pin."""
        pass

    @abstractmethod
    def get_analog_output(self, pin: int) -> BaseAnalogOutput:
        """Get an analog output pin."""
        pass

    @abstractmethod
    def read_adc(self, channel: int) -> float:
        """Read the analog input pin."""
        pass

    @abstractmethod
    def read_all_adcs(self) -> list[float]:
        """Read all analog input pins."""
        pass


class BaseInterruptManager(ABC):
    """Base class for managing the interrupt callbacks for a piplate
    
    The piplate offers multiple interrupts but all will set a bit in the
    interrupt byte on the plate and pull pin 20 on the rpi low. This class
    will read the interrupt byte and call the appropriate callback.
    """

    @abstractmethod
    def reset_register(self) -> ...:
        """Reset the interrupt register on the plate.
        
        This will not remove the callbacks, just reset the register
        on the piplate.
        """
        pass

    @abstractmethod
    def register_callback(self, index: int, callback: callable) -> ...:
        """Register a callback for an interrupt on 'index' in the interrupt byte.
        
        The callback will be called when the interrupt is triggered.
        """
        pass

    @abstractmethod
    def unregister_callback(self, index: int) -> ...:
        """Unregister the callback for an interrupt on 'index' in the interrupt byte.
        
        The callback will no longer be called when the interrupt is triggered.
        """
        pass

    @abstractmethod
    def unregister_all_callbacks(self) -> ...:
        """Unregister all callbacks.
        
        No callbacks will be called when the interrupt is triggered.
        """
        pass

    @abstractmethod
    def run(self) -> ...:
        """Run the interrupt manager.
        
        This will enable the interrupt pin on the rpi and call the callbacks
        when the interrupt is triggered.
        """
        pass

    @abstractmethod
    def stop(self) -> ...:
        """Stop the interrupt manager.
        
        This will stop the interrupt pin on the rpi and no callbacks will be
        called when the interrupt is triggered.
        """
        pass



