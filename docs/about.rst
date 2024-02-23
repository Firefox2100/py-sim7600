================
About py-sim7600
================

State of development
====================

Current version: **0.1.0-alpha.1**

This package is still in alpha stage, and no release will be generated for now. The major functions are still incomplete, and the completed functions are not guarenteed to work. For now this package will not be uploaded to PyPI, so if you really want to use it now, please install with git.

**Important**: I will only update the PyPI version when there is a change in usage, like bug fixes or feature updates. For code restructure, clean-up, documents modification, etc. I won't update the version. So please note that source installed from ``pip`` and pulled from GitHub may not be the same.

-------
Roadmap
-------

The achieved features and steps are:

- Basic ability to communicate with SIM7600 modules.
- PyPI module package
- Pytest suite designed
- Commands according to V.25TER

The (currently) planned features are:

- Full AT command list support
- A detailed interface design for SIM-ME interface
- A class for integrated functions (call, text, answer, data connection, phone book, etc.)

The (currently) planned steps are:

- Usage of this library with other SIMCom modules

The features or steps that are not planned to implement are:

- Any form of application support (the ability to run this library directly as backend, server, etc.)

Contribution
============

Currently, this project is developed and maintained by myself. It's too large a project for me to finish alone, so any form of help is welcomed. However, please do not donate. Instead, I'd be more than happy if you could help with develop, debug, testing, or even just give me suggestions. Feel free to email me through GitHub, or any other contact method.

------------
Bug tracking
------------

The bug tracking should be in this repository as issues. Feel free to open an issue for bugs or suggestions, but please properly tag it, and check if there are duplications. There are templates for issues created, but if it doesn't fit the purpose, feel free to write another one.

------------
Pull request
------------

You can open any pull request without contacting me. Any improvements to this project is welcomed, and I'll merge them as fast as I could, if there are no conflictions or bugs in the pull request.
