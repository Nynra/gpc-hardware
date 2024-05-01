import configparser
from typing import Union
from ast import literal_eval
import os


class Settings:
    """
    Class to handle the settings.

    Class manages the information in the hardware_config.ini file.
    The sections are named as follows:
        <type>.<id>

    Where <id> is the part ID and not the id in the system (axis id).

    The config first looks in the <type>.<id> section and then in the
    <type>.DEFAULT section for fallback values. If the key is not found
    in either section, a KeyError is raised.
    """

    def __init__(self, filename: str = "default.ini") -> None:
        """
        Initialize the settings.

        Parameters
        ----------
        filename: str
            The filename of the settings file.
        """
        self._config = configparser.ConfigParser()

        # Create the path to file
        self._filename = filename
        path = os.path.dirname(os.path.abspath(__file__)) + "\\" + self._filename

        # Check if the file exists
        if not self._file_exists(path):
            raise FileNotFoundError(f"File {path} not found.")

        # Load the settings
        self._config.read(path)

    # FUNCTIONS
    @staticmethod
    def _file_exists(filename: str) -> bool:
        """
        Check if a file exists.

        Parameters
        ----------
        filename: str
            The filename to check.

        Returns
        -------
        exists: bool
            True if the file exists, False otherwise.
        """
        try:
            with open(filename, "r") as f:
                pass
            return True
        except FileNotFoundError:
            return False

    def get(self, section: str, key: str) -> Union[str, int, float, bool]:
        """
        Get the value of a key in a specific section.

        Will look in the given section first and uses the type.DEFAULT section
        for fallback values.

        Parameters
        ----------
        section: str
            The section to look in.
        key: str
            The key to look for.

        Raises
        ------
        KeyError
            If the key is not found in the given section or the default section.

        Returns
        -------
        value: str, int, float, bool
            The value of the key.
        """
        val = self._config.get(section, key, fallback=None)
        if val is None:  # Look in the default section
            val = self._config.get(
                section.split(".")[0] + ".DEFAULT", key, fallback=None
            )

        if val is None:  # Key not found
            raise KeyError(f"Key {key} not found in section {section}")

        try:
            val = literal_eval(val)
        except ValueError:
            pass

        return val

    def set(self, section: str, key: str, value: Union[str, int, float, bool]) -> None:
        """
        Set the value of a key in a specific section.

        .. attention::

            It is not allowed to change settings in DEFAULT sections.
            If the setting should be changed this had to be done by hand
            in the settings file.

        Parameters
        ----------
        section: str
            The section to look in.
        key: str
            The key to look for.
        value: str, int, float, bool
            The value to set the key to.

        Raises
        ------
        KeyError
            If the user tries to change a setting in the DEFAULT section.
        """
        # Check if the section is a DEFAULT section
        if section.split(".")[-1] == "DEFAULT":
            raise KeyError(f"Changing settings in DEFAULT sections is not allowed.")

        if section not in self._config.sections():
            raise KeyError(f"Section {section} not found.")

        # Set the value
        self._config[section][key] = str(value)

    def save(self, filename: Union[str, None] = None) -> None:
        """Save the settings to the file."""
        if filename is None:
            filename = self._filename
        path = os.path.dirname(os.path.abspath(__file__)) + "\\" + filename
        with open(path, "w") as configfile:
            self._config.write(configfile)


if __name__ == "__main__":
    settings = Settings()
