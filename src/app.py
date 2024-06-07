import asyncio
import logging
import sys
from os import getenv
from urllib.parse import quote

import aiohttp
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from bs4 import BeautifulSoup

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

async def get_weather(city) -> str:
    url = "https://www.google.com/search?q=" + quote("погода в" + city)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}) as response:
            soup = await response.text()
            bs = BeautifulSoup(soup, "html.parser")
            weather = bs.find("span", {"id": "wob_tm"})
            if weather:
                return  weather.text
            else:
                return "Не удалось получить погоду"





@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def message_handler(message: Message) -> None:
    try:
        weather = await get_weather(message.text)
        await  message.answer(weather)
    except Exception:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Error")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(
        token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
