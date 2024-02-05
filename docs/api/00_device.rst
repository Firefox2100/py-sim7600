.. _topics_00_device:

======
Device
======

The :code:`Device` class is an interface to communicate with the SIM7600 modem. This file may raise SIM7600Exception, or any other unintended exceptions due to unforseen error. For more details with exceptions, please refer to :ref:`_topics_00_exception`.

Classes
=======

------
Device
------

Class to communicate directly with SIM7600 device.

Member variables
----------------

This class contains following member variables:
    - `__port`: String. Port to use to communicate with the SIM7600 modem. It has to be the full path of the port, i.e. `/dev/ttyACM0` or `COM2`
    - `__is_rpi`: Boolean. To denote whether this device is a Raspberry Pi. This is done by tring to import a RPi-specific library `RPi.GPIO`.
    - `__serial`: serial.Serial. An instance of serial device, assigned to the designated serial port.
    - `__power_key`: Integer. The GPIO number for power key used in some SIM7600 modules.
    - `__is_on`: Boolean. A variable to denote whether the modem is on. This only matters if this script is run on RPi, **AND** the modem has the hardware pin to control ON/OFF.
    - `__buffer`: String. A buffer for serial port results.

Constructor
-----------

.. code-block:: python
    def __init__(self, port: str, baud=115200):

Parameters:
    - `port`: String. The serial port to use.
    - `baud`: Integer. The baud rate to set the serial port to. Default is 115200.
Usage:
    .. code-block:: python

        Device("/dev/ttyACM2", 115200)

result
------

.. code-block:: python

    def result(self) -> str:

