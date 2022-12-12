# py-sim7600

This is a PyPI package to interface with SIM7600 modems.

## Disclaimer

This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this software. If not, see http://www.gnu.org/licenses/.

This project also utilizes third part libraries and tools, like Python, py-serial, etc. They are listed under separate licenses, and their copyright and credit should goes to their original authors. This software will not distribute these source code or executables in any form.

Please note that not all operations and modifications with SIM7600 are legal in all countries and regions. Use this project at your own discretion.

## Introduction

This library provides a way to communicate and control SIM7600 modems with pure python.

### Requirements

To use this library you will need:

- A compatible SIM7600 development board. This library communicates to the modem with serial port, so the module must be able to accept standart ``AT`` commands from serial connection. Any custom made or modified modules that use custom client or differnet command set will NOT be supported. This library is known to work will all Waveshare SIM7600 modems.
- A Python environment >= 3.7.
- Access to serial port. Make sure your machine has serial port, andthe user to execute this library has the access right to it. In some OS it might be necessary to install drivers.

### Usage

The documents are being written and reviewed.

### Installation

This module can either be downloaded as a library folder and placed under your Python path, or install as a PyPI package. Run:

```shell
pip install git+https://github.com/Firefox2100/py-sim7600
```

To install the package. In the future, this package **might** be uploaded to PyPI.

## State of development

Current version: **Pre-Aplha 0.1.0**

This package is still in pre-alpha stage, and no release will be generated for now. The major functions are still incomplete, and the completed functions are not guarenteed to work. For now this package will not be uploaded to PyPI, so if you really want to use it now, please install with git.

### Roadmap

The achieved features and steps are:

- Basic ability to communicate with SIM7600 modules.
- PyPI module package
- Commands according to V.25TER

The (currently) planned features are:

- Full AT command list support
- A class for integrated functions (call, text, answer, data connection, phone book, etc.)

The (currently) planned steps are:

- Pytest suite design

The features or steps that are not planned to implement are:

- Any form of application support (the ability to run this library directly as backend, server, etc.)
