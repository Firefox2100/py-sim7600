.. _topics_00_exception:

==========
Exceptions
==========

This file `error.py` contains custom classes for exceptions raised in this module.

Classes
=======

----------------
SIM7600Exception
----------------

Exception raised by SIM7600 device commands.

Constructor
-----------

.. code-block:: python
    def __init__(self, message: str, errors=''):

Parameters
    - message: String, the message to be displayed in exceptions.
    - errors: String, the detailed error information (if any).
Usage
    .. code-block:: python
        raise SIM7600Exception('Some Exception happened', 'Parameter can\'t be ' + x.toString())

---------------
V25TERException
---------------

Exception raised by V25TER commands.

Constructor
-----------

.. code-block:: python
    def __init__(self, message: str, errors=''):

Parameters
    - message: String, the message to be displayed in exceptions.
    - errors: String, the detailed error information (if any).
Usage
    .. code-block:: python
        raise V25TERException('Some Exception happened', 'Parameter can\'t be ' + x.toString())

----------------------
StatusControlException
----------------------

Exception raised by status control commands.

Constructor
-----------

.. code-block:: python
    def __init__(self, message: str, errors=''):

Parameters
    - message: String, the message to be displayed in exceptions.
    - errors: String, the detailed error information (if any).
Usage
    .. code-block:: python
        raise StatusControlException('Some Exception happened', 'Parameter can\'t be ' + x.toString())

----------------
NetworkException
----------------

Exception raised by network commands.

Constructor
-----------

.. code-block:: python
    def __init__(self, message: str, errors=''):

Parameters
    - message: String, the message to be displayed in exceptions.
    - errors: String, the detailed error information (if any).
Usage
    .. code-block:: python
        raise NetworkException('Some Exception happened', 'Parameter can\'t be ' + x.toString())

--------------------
CallControlException
--------------------

Exception raised by call control commands.

Constructor
-----------

.. code-block:: python
    def __init__(self, message: str, errors=''):

Parameters
    - message: String, the message to be displayed in exceptions.
    - errors: String, the detailed error information (if any).
Usage
    .. code-block:: python
        raise CallControlException('Some Exception happened', 'Parameter can\'t be ' + x.toString())
