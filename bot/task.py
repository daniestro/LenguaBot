import json

from database import add_task
from rabbit_queue import add_to_queue


class Task:

    def __init__(self, user_id: str, word_id: str, chat_id: int, message: str) -> None:
        self.user_id = user_id
        self.word_id = word_id
        self.chat_id = chat_id
        self.message = message

    @staticmethod
    def clear_html_tags(message: str) -> str:
        empty = ''
        htmls_tags = ['<b>', '</b>']
        for tag in htmls_tags:
            message = message.replace(tag, empty)
        return message

    async def _add_to_db(self) -> None:
        await add_task(self.user_id, self.word_id, self.clear_html_tags(self.message))

    async def create(self) -> None:
        await self._add_to_db()
        await self._add_to_queue()

    async def _add_to_queue(self) -> None:
        await add_to_queue(
            self._convert(
                chat_id=self.chat_id,
                message=self.message
            )
        )

    @staticmethod
    def _convert(**kwargs) -> str:
        return json.dumps({**kwargs})
