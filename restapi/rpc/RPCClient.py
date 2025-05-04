"""
RabbitMQ RPC Client

based off of https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/6-rpc.html
"""

import asyncio
import logging
from typing import MutableMapping, Optional
from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractIncomingMessage, AbstractQueue
import uuid

from .RPCResponse import RPCResponse


class Client:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop

    def __init__(self, uri: str) -> None:
        """
        Init
        :param uri: Connection URI
        """
        self.__uri = uri
        self.futures: MutableMapping[str, asyncio.Future] = {}

    async def connect(self) -> "Client":
        """
        Connect to RabbitMQ
        :return: Client
        """
        self.loop = asyncio.get_running_loop()
        self.connection = await connect_robust(self.__uri, loop=self.loop)
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue()
        await self.callback_queue.consume(self.on_response)
        return self

    async def on_response(self, message: AbstractIncomingMessage) -> None:
        """
        On response from RPC consumer
        :param message: Incoming message
        :return: Dict/List response
        """
        if message.correlation_id is None:
            logging.error(f"Bad RPC Response: {message!r}")
            return
        future: asyncio.Future = self.futures.pop(message.correlation_id)
        await message.ack()
        future.set_result(
            {
                "data": message.body,
                "headers": message.headers,
                "content_type": message.content_type,
                "msg_type": message.type,
                "content_encoding": message.content_encoding,
                "expiration": message.expiration,
                "timestamp": message.timestamp,
                "user_id": message.user_id,
                "app_id": message.app_id,
            }
        )

    async def call(
        self, routing_key: str, payload: bytes, content_type: str, timeout: Optional[int] = None
    ) -> RPCResponse:
        """
        Send RPC Call
        :param content_type:
        :param timeout: Optional Timeout
        :param routing_key: routing key for RabbitMQ
        :param payload: Message payload dict or list
        :return: Dict response from consumer
        """
        future = self.loop.create_future()  # Holds call state
        correlation_id = str(uuid.uuid4())
        self.futures[correlation_id] = future
        # Create bytes payload
        await self.channel.default_exchange.publish(
            Message(
                payload,
                content_type=content_type,
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
                expiration=timeout,
            ),
            routing_key=routing_key,
        )
        if timeout is None:
            return await future
        return RPCResponse[bytes](**(await asyncio.wait_for(future, timeout=timeout)))

    async def one_way_call(self, routing_key: str, payload: bytes, content_type: str) -> None:
        """
        Send RPC Call with no expectation of reply
        :param content_type:
        :param routing_key: routing key for RabbitMQ
        :param payload: Message payload as bytes
        :return: None
        """
        # Create bytes payload
        await self.channel.default_exchange.publish(
            Message(
                payload,
                content_type=content_type,
            ),
            routing_key=routing_key,
        )
