from aio_pika import connect, Message

from settings import rabbit_settings


DIRECT = 'direct'
ENCODING = 'utf-8'
CONTENT_TYPE = 'text/plain'


async def get_connection_data():
    connection = await connect(rabbit_settings.url)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(DIRECT, auto_delete=True)
    return connection, channel, exchange


async def create_queue() -> None:
    connection, channel, exchange = await get_connection_data()
    queue = await channel.declare_queue(rabbit_settings.rabbit.QUEUE_NAME, auto_delete=True)
    await queue.bind(exchange, routing_key=rabbit_settings.rabbit.ROUTING_KEY)


async def add_to_queue(data: str) -> None:
    connection, channel, exchange = await get_connection_data()
    await exchange.publish(
        Message(
            bytes(data, ENCODING),
            content_type=CONTENT_TYPE,
            headers={'foo': 'bar'}
        ),
        routing_key=rabbit_settings.rabbit.ROUTING_KEY
    )
