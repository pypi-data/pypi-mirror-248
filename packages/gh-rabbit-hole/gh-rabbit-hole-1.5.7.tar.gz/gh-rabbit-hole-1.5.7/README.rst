AsyncioRabbitManager
====================

The ``AsyncioRabbitManager`` class provides an asynchronous interface
for connecting and interacting with RabbitMQ using Python and asyncio.
Designed for applications requiring reactive and non-blocking
processing, this class manages the connection to RabbitMQ, sending and
receiving messages, and declaring exchanges and queues, all
asynchronously.

Features
--------

-  **Asynchronous Connection:** Establishes non-blocking connections to
   RabbitMQ, allowing the rest of the application to continue executing
   while managing network operations in the background.
-  **Channel Management:** Opens and configures RabbitMQ channels to
   send and receive messages.
-  **Message Sending and Receiving:** Supports sending messages to
   queues or exchanges and configuring asynchronous callbacks for
   incoming message handling.
-  **Asyncio Integration:** Built around asyncio primitives for easy
   integration with other asynchronous operations and the event loop.
-  **Advanced Logging:** Utilizes a customizable logging system to
   monitor activities and quickly diagnose issues.

Usage
-----

Ideal for asyncio-based applications that require efficient and
asynchronous communication with RabbitMQ. Especially useful in contexts
where performance and responsiveness are critical, such as in
microservices, bots, or real-time data processing systems.

Initialization
~~~~~~~~~~~~~~

.. code:: python

   import logging
   from your_module import AsyncioRabbitManager  # Replace with the actual module name

   logger = logging.getLogger(__name__)

   rabbit_manager = AsyncioRabbitManager(
       amqp_url="your_amqp_url",
       sending_queue="your_sending_queue",
       listening_queue="your_listening_queue",
       sending_exchange="your_sending_exchange",
       logger=logger,
       on_message_callback=your_message_callback_function  # Replace with your callback
   )

Connecting to RabbitMQ
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   import asyncio

   async def main():
       await rabbit_manager.connect()

   asyncio.run(main())

Sending Messages
~~~~~~~~~~~~~~~~

.. code:: python

   message = {"key": "value"}  # Your message content
   routing_key = "your_routing_key"  # Optional
   to_exchange = False  # Set to True if sending to an exchange

   rabbit_manager.send_message(message, routing_key, to_exchange)

Receiving Messages
~~~~~~~~~~~~~~~~~~

Implement your message handling logic in a callback function:

.. code:: python

   async def message_handler(channel, method, properties, body):
       print("Received message:", body)

   # Set this as your callback
   rabbit_manager.on_message_callback = message_handler

Closing the Connection
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   async def close():
       await rabbit_manager.close_connection()

   asyncio.run(close())

Installation
------------

Ensure you have ``pika`` and ``asyncio`` installed:

.. code:: shell

   pip install pika asyncio

License
-------

MIT License

Copyright (c) 2023 Massimo Ghiani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


--------------

This README provides a basic overview and examples for the
``AsyncioRabbitManager`` class. Adjust the content to fit the specifics
of your implementation and environment.
