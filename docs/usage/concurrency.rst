.. _topics-usage-concurrency:

====================
Managing Concurrency
====================

SIM7600 (or any SIMCom module) is a serial device, exposing 1-2 serial ports for AT command interface. In normal conditions, only one process can use one serial port at a time. This is the base assumption this library is developed on. However, Python libraries are not always used in a single-threaded, concurrent environment. This section will discuss how to manage concurrency in different scenarios.

**This is very important, as not following these guidelines can lead to unexpected behavior, including hardware damage and SIM card damage.**

Single-threaded use
===================

In a single-threaded environment, this library behaves as expected. You can use the library directly, without the need to modify or configure anything.

Asynchronous use
================

Some libraries, like ``asyncio``, are designed to work in single thread, single process, but asynchronous context, where some functions may not be awaited and the control is returned to the event loop. This library will not break in such context, but it's fully synchronous, and will block the event loop when waiting for a response from the device. Even if the functions from this library is wrapped in a coroutine, the locking mechanism will still prevent multiple access to the serial port. For example:

.. code-block:: python

    import asyncio
    from py_sim7600.device.sim7600 import SIM7600Device

    device = SIM7600Device('/dev/ttyUSB2')

    async def send_test_command():
        device.send('AT', back='OK')

    async def main():
        await asyncio.gather(send_test_command(), send_test_command())

In the above example, the ``device.send()`` method, due to internal locking mechanism, will obtain a lock for the serial device, thus the second call to ``send_test_command()`` will block until the first one is finished. This is the expected behavior, and it's the correct way to handle this situation. You do not need to manually adjust the library or to adapt the code for asynchronous use.

Multi-threaded use
==================

*This is only a concern if the communication to the device happens in multiple threads. It won't be a problem if the device is communicated in the main thread, while the other threads do something else. Same applies to the other scenarios.*

The library uses ``threading.Semaphore`` to manage access to the serial port. This means that if you use the library in multiple threads, the threads will block each other when trying to access the serial port. This is the expected behavior, and it's the correct way to handle this situation. You do not need to manually adjust the library or to adapt the code for multi-threaded use.

However, you need to be aware of this behavior, and to design your application accordingly. This could lower the performance of multi-threaded applications, as the threads will block each other when trying to access the serial port. Also, a dead-lock prevention mechanism should be in place in your application, in case the serial port is blocked by another thread. The library will always release the lock after the execution of a read or write operation.

Multi-process use
=================

The ``threading.Semaphore`` is not multi-process safe, as the lock is not shared automatically between processes. I would recommend using ``multiprocessing.Lock`` instead in a multi-process environment. Note that the initialization of the lock should be done before the sub-processes are forked, and the lock should be passed to the sub-processes. To use the lock:

.. code-block:: python

    import multiprocessing
    from py_sim7600.device import Device

    lock = multiprocessing.Lock

    Device.set_lock(lock)                   # This set the lock class as a class variable
    Device.initialize_lock('your_port')     # This initializes the lock

    # Your fork code here

This also applies to any web server based on workers, daemon, or other multi-process framework that does not explicitly share the lock between processes. They should provide a callback, or some other method to run code before forking happens. Refer to their documentation for more information.
