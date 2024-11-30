from aio_pika import connect
from aio_pika.abc import AbstractMessage

from settings import rabbit_settings


DIRECT = 'direct'
ENCODING = 'utf-8'
CONTENT_TYPE = 'text/plain'


async def get_message_from_queue() -> AbstractMessage:
    connection = await connect(rabbit_settings.url)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(DIRECT, auto_delete=True)
    queue = await channel.declare_queue(rabbit_settings.rabbit.QUEUE_NAME, auto_delete=True)
    await queue.bind(exchange, routing_key=rabbit_settings.rabbit.ROUTING_KEY)
    incoming_message = await queue.get(timeout=5)
    await incoming_message.ack()
    return incoming_message
