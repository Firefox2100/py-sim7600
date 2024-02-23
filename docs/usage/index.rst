.. _topics-usage-index:

=============
Library Usage
=============

This section provides a guide on how to use the library.

.. toctree::
    :maxdepth: 3
    :caption: Contents:

    quickstart
    concurrency

.. warning::
    SIM7600 is a serial device, and it is important to note that the serial port should, and can only be accessed by one process at a time. Normally in OS, this is achieved by preventing other processes from opening the port. However, if this library is to be used in a multi-threaded or multi-process environment, it's very important to handle concurrent access to the serial port properly. This could lead to **data corruption, device malfunction, or even damage**. Read the :ref:`topics-usage-concurrency` section for more information before using the library in a multi-threaded or multi-process environment.
