import json
from enum import Enum
from typing import Callable

import pika
from pika import exceptions
from retry import retry


class Queue:
    class QueueBinding:
        exchange: str
        routing_key: str

        def __init__(self, exchange: str, routing_key: str = '*') -> None:
            self.exchange = exchange
            self.routing_key = routing_key

    name: str
    bindings: list[QueueBinding]

    def __init__(self, name: str, bindings: list[QueueBinding] = None) -> None:
        self.name = name
        self.bindings = bindings or []


class Snowshoe:
    connection: pika.BlockingConnection
    channel: pika.adapters.blocking_connection.BlockingChannel
    name: str

    class AckMethod(Enum):
        OFF = 0
        ON_FETCH = 1
        ON_SUCCESS = 2

    def __init__(self, name, host: str, port: int, username: str, password: str) -> None:
        self.name = name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(
                username=username,
                password=password
            )
        ))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.name, 'topic')

    @retry(exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def start(self):
        self.channel.start_consuming()

    def define_queues(self, queues: list[Queue]):
        for queue in queues:
            self.channel.queue_declare(queue.name)
            for binding in queue.bindings:
                self.channel.queue_bind(queue.name, binding.exchange, binding.routing_key)

    def emit(self, topic: str, data: dict):
        return self.channel.basic_publish(exchange=self.name, routing_key=topic, body=json.dumps(data).encode())

    def on(self, queue: str, ack_method: AckMethod = AckMethod.ON_SUCCESS):
        def wrapper(handler: Callable[[dict, str, str], any]):
            def callback(
                    _channel: pika.adapters.blocking_connection.BlockingChannel,
                    method: pika.spec.Basic.Deliver,
                    _properties: pika.spec.BasicProperties,
                    body: bytes
            ):
                result = handler(method.routing_key, json.loads(body), method.delivery_tag)
                if ack_method == Snowshoe.AckMethod.ON_SUCCESS:
                    self.channel.basic_ack(method.delivery_tag)
                return result

            self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=ack_method == Snowshoe.AckMethod.ON_FETCH)

        return wrapper
