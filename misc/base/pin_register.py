from threading import Lock


class PinRegister:
    """Class for keeping track of which pins are used."""

    def __init__(self, din: int = 7, dout: int = 7, ain: int = 7, aout: int = 3):
        """Initialize the PinRegister."""
        if not isinstance(din, int):
            raise TypeError(f"din must be an integer, not type {type(din)}")
        if not isinstance(dout, int):
            raise TypeError(f"dout must be an integer, not type {type(dout)}")
        if not isinstance(ain, int):
            raise TypeError(f"ain must be an integer, not type {type(ain)}")
        if not isinstance(aout, int):
            raise TypeError(f"aout must be an integer, not type {type(aout)}")

        self._lock = Lock()
        self._digital_inputs = din
        self._digital_outputs = dout
        self._analog_inputs = ain
        self._analog_outputs = aout

        self._pins = {
            "digital_inputs": [],
            "digital_outputs": [],
            "analog_inputs": [],
            "analog_outputs": [],
        }

    def register_digital_input(self, pin: int) -> ...:
        """Register a digital input pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (0 <= pin <= self._digital_inputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin in self._pins["digital_inputs"]:
            raise ValueError(f"Pin {pin} is already registered")
        with self._lock:
            self._pins["digital_inputs"].append(pin)

    def register_digital_output(self, pin: int) -> ...:
        """Register a digital output pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (0 <= pin <= self._digital_outputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin in self._pins["digital_outputs"]:
            raise ValueError(f"Pin {pin} is already registered")
        with self._lock:
            self._pins["digital_outputs"].append(pin)

    def register_analog_input(self, pin: int) -> ...:
        """Register an analog input pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (0 <= pin <= self._analog_inputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin in self._pins["analog_inputs"]:
            raise ValueError(f"Pin {pin} is already registered")
        with self._lock:
            self._pins["analog_inputs"].append(pin)

    def register_analog_output(self, pin: int) -> ...:
        """Register an analog output pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (1 <= pin <= self._analog_outputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin in self._pins["analog_outputs"]:
            raise ValueError(f"Pin {pin} is already registered")
        with self._lock:
            self._pins["analog_outputs"].append(pin)

    def unregister_digital_input(self, pin: int, raise_exceptions: bool = True) -> ...:
        """Unregister a digital input pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (0 <= pin <= self._digital_inputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin not in self._pins["digital_inputs"]:
            if raise_exceptions:
                raise ValueError(f"Pin {pin} is not registered")
            return
        with self._lock:
            self._pins["digital_inputs"].remove(pin)

    def unregister_digital_output(self, pin: int, raise_exceptions: bool = True) -> ...:
        """Unregister a digital output pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (0 <= pin <= self._digital_outputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin not in self._pins["digital_outputs"]:
            if raise_exceptions:
                raise ValueError(f"Pin {pin} is not registered")
            return
        with self._lock:
            self._pins["digital_outputs"].remove(pin)

    def unregister_analog_input(self, pin: int, raise_exceptions: bool = True) -> ...:
        """Unregister an analog input pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (0 <= pin <= self._analog_inputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin not in self._pins["analog_inputs"]:
            if raise_exceptions:
                raise ValueError(f"Pin {pin} is not registered")
            return
        with self._lock:
            self._pins["analog_inputs"].remove(pin)

    def unregister_analog_output(self, pin: int, raise_exceptions: bool = True) -> ...:
        """Unregister an analog output pin"""
        if not isinstance(pin, int):
            raise TypeError(f"Pin must be an integer, not type {type(pin)}")
        if not (1 <= pin <= self._analog_outputs):
            raise ValueError(f"Invalid pin: {pin}")
        if pin not in self._pins["analog_outputs"]:
            if raise_exceptions:
                raise ValueError(f"Pin {pin} is not registered")
            return
        with self._lock:
            self._pins["analog_outputs"].remove(pin)

    def get_pins(self) -> dict:
        """Get all registered pins"""
        with self._lock:
            return self._pins
