# py-sim7600

This is a PyPI package to interface with SIM7600 modems.

## Disclaimer

This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this software. If not, see http://www.gnu.org/licenses/.

This project also utilizes third part libraries and tools, like Python, py-serial, etc. They are listed under separate licenses, and their copyright and credit should go to their original authors. This software will not distribute these source code or executables in any form.

Please note that not all operations and modifications with SIM7600 are legal in all countries and regions. Use this project at your own discretion.

## Introduction

This library provides a way to communicate and control SIM7600 modems with pure python.

### Requirements

To use this library you will need:

- A compatible SIM7600 development board. This library communicates to the modem with serial port, so the module must be able to accept standard ``AT`` commands from serial connection. Any custom-made or modified modules that use custom client or different command set will NOT be supported. This library is known to work will all WaveShare SIM7600 modems.
- A Python environment >= 3.7.
- Access to serial port. Make sure your machine has serial port, and the user to execute this library has the access right to it. In some OS it might be necessary to install drivers.

### Usage

The documents are being written and reviewed.

### Installation

This module can either be downloaded as a library folder and placed under your Python path, or install as a PyPI package. Run:

```shell
pip install git+https://github.com/Firefox2100/py-sim7600
```

To install the package. In the future, this package **might** be uploaded to PyPI.

## State of development

Current version: **Pre-Alpha 0.1.0**

This package is still in pre-alpha stage, and no release will be generated for now. The major functions are still incomplete, and the completed functions are not guaranteed to work. For now this package will not be uploaded to PyPI, so if you really want to use it now, please install with git.

### Roadmap

The achieved features and steps are:

- Basic ability to communicate with SIM7600 modules.
- PyPI module package
- Commands according to V.25TER

The (currently) planned features are:

- Full AT command list support
- A detailed interface design for SIM-ME interface
- A class for integrated functions (call, text, answer, data connection, phone book, etc.)

The (currently) planned steps are:

- Pytest suite design

The features or steps that are not planned to implement are:

- Any form of application support (the ability to run this library directly as backend, server, etc.)

## Contribution

Currently this project is developed and maintained by myself. It's too large a project for me to finish alone, so any form of help is welcomed. However, please do not donate. Instead, I'd be more than happy if you could help with develop, debug, testing, or even just give me suggestions. Feel free to email me through GitHub, or any other contact method.

### Bug tracking

The bug tracking should be in this repository as issues. Feel free to open an issue for bugs or suggestions, but please properly tag it, and check if there are duplications. There are templates for issues created, but if it doesn't fit the purpose, feel free to write another one.

### Pull request

You can open any pull request without contacting me. Any improvements to this project is welcomed, and I'll merge them as fast as I could, if there's no conflict or bugs in the pull request.
