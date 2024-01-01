Asyncio Rabbit Manager
======================

An advanced Python package to asynchronously manage RabbitMQ
connections, queues, and message handling using asyncio. Ideal for
high-performance, non-blocking applications.

Features
--------

-  **Asynchronous Operations**: Utilize the full potential of asyncio
   for non-blocking message sending and receiving.
-  **Customizable Logging**: Leverage colored logs for better monitoring
   and debugging.
-  **Connection Resilience**: Automatically reconnects in case of
   connection failures.
-  **Message Handling**: Send and receive messages asynchronously with
   optional callbacks.
-  **Factory Design**: Utilize the factory pattern for creating
   instances with various configurations.

Installation
------------

Install the package via pip:

.. code:: bash

   pip install asyncio-rabbit-manager

Usage
-----

Basic Setup
~~~~~~~~~~~

First, import the necessary classes:

.. code:: python

   from asyncio_rabbit_manager import AsyncioRabbitManagerFactory, AsyncioRabbitManager

Creating a Manager
~~~~~~~~~~~~~~~~~~

Use the factory to create an instance of ``AsyncioRabbitManager``:

.. code:: python

   factory = AsyncioRabbitManagerFactory()
   rabbit_manager = factory.create('<config_file_name>')

Sending Messages
~~~~~~~~~~~~~~~~

Send messages to a specified queue:

.. code:: python

   rabbit_manager.send_message('Hello, World!', 'my_queue')

Receiving Messages
~~~~~~~~~~~~~~~~~~

Define a callback for incoming messages and start listening:

.. code:: python

   async def handle_message(channel, method, properties, body):
       print("Received message:", body)

   rabbit_manager.on_message_callback = handle_message
   await rabbit_manager.connect()

Closing Connection
~~~~~~~~~~~~~~~~~~

Properly close the connection when done:

.. code:: python

   await rabbit_manager.close_connection()

Advanced Usage
--------------

The ``AsyncioRabbitManager`` class provides an asynchronous interface
for connecting and interacting with RabbitMQ using Python and asyncio.
Designed for applications requiring reactive and non-blocking
processing, this class manages the connection to RabbitMQ, sending and
receiving messages, and declaring exchanges and queues, all
asynchronously.

.. _features-1:

Features
~~~~~~~~

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

.. _usage-1:

Usage
~~~~~

Ideal for asyncio-based applications that require efficient and
asynchronous communication with RabbitMQ. Especially useful in contexts
where performance and responsiveness are critical, such as in
microservices, bots, or real-time data processing systems.

Initialization
^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   import asyncio

   async def main():
       await rabbit_manager.connect()

   asyncio.run(main())

.. _sending-messages-1:

Sending Messages
^^^^^^^^^^^^^^^^

.. code:: python

   message = {"key": "value"}  # Your message content
   routing_key = "your_routing_key"  # Optional
   to_exchange = False  # Set to True if sending to an exchange

   rabbit_manager.send_message(message, routing_key, to_exchange)

.. _receiving-messages-1:

Receiving Messages
^^^^^^^^^^^^^^^^^^

Implement your message handling logic in a callback function:

.. code:: python

   async def message_handler(channel, method, properties, body):
       print("Received message:", body)

   # Set this as your callback
   rabbit_manager.on_message_callback = message_handler

Closing the Connection
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   async def close():
       await rabbit_manager.close_connection()

   asyncio.run(close())

Contributing
------------

Contributions, issues, and feature requests are welcome!

License
-------

Distributed under the MIT License. See ``LICENSE`` for more information.

Contact
-------

Massimo Ghiani - m.ghiani@gmail.com

Project Link: https://github.com/m-ghiani/RABBIT_HOLE
