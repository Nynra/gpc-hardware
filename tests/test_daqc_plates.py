from unittest import TestCase
# from piplates.DAQC2plate import DAQC2
from gpc_hardware.utils.piplates.DAQC2plate import DAQC2


class TestDaqc2Plate(TestCase):
    """Check if the Pi is connected to the DAQC2"""

    def test_daqc2_plate(self):
        daqc = DAQC2(0)


