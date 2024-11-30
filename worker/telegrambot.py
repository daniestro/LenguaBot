import aiohttp

from settings import bot_settings


async def send_message(message: dict) -> None:
    url = f'https://api.telegram.org/bot{bot_settings.TOKEN}/sendMessage'
    data = {'chat_id': message['chat_id'], 'text': f'Maybe u want to practise with word {message['word']}'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()
