import asyncio
import logging
import sys
import json

from aio_pika.exceptions import QueueEmpty

from rabbit_queue import get_message_from_queue
from telegrambot import send_message


logger = logging.getLogger(__name__)


async def processing_messages_task() -> None:
    while True:
        try:
            message = await get_message_from_queue()
            encoded_message = json.loads(message.body)
            logger.info(f"Message received: {encoded_message}?")
            response = await send_message(encoded_message)
            logger.info(response)
        except QueueEmpty:
            logger.info('Queue is empty')
            await asyncio.sleep(15)


async def main() -> None:
    processing_task = asyncio.create_task(processing_messages_task())
    await processing_task


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )
    asyncio.run(main())
