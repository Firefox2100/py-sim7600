.. py-sim7600 documentation master file, created by
   sphinx-quickstart on Mon Dec 19 14:11:05 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================================
Py-SIM7600 Documentation
======================================

py-sim7600 is a PyPI package for interfacing with standard SIM7600 modems that support ``AT`` commands.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   about
   /api/index

Disclaimer
==========

This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this software. If not, see http://www.gnu.org/licenses/.

This project also utilizes third part libraries and tools, like Python, py-serial, etc. They are listed under separate licenses, and their copyright and credit should goes to their original authors. This software will not distribute these source code or executables in any form.

Please note that not all operations and modifications with SIM7600 are legal in all countries and regions. Use this project at your own discretion.

Requirements
============

To use this library you will need:

- A compatible SIM7600 development board. This library communicates to the modem with serial port, so the module must be able to accept standard ``AT`` commands from serial connection. Any custom made or modified modules that use custom client or differnet command set will NOT be supported. This library is known to work will all Waveshare SIM7600 modems.
- A Python environment >= 3.7.
- Access to serial port. Make sure your machine has serial port, andthe user to execute this library has the access right to it. In some OS it might be necessary to install drivers.

Install
=======

Currently, this package is in **Pre-Alpha** stage, so it's not recommended for users to start using it now, as there are bugs and potential fatal errors in the code. It's also the reason why this package is not uploaded to PyPI, so to use it now, users will need to install from git:

.. code-block:: bash
   
   pip install git+https://github.com/Firefox2100/py-sim7600

Usage
=====

This package is still under active development. No usage documentation, or interfaces designed for end users are provided.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
