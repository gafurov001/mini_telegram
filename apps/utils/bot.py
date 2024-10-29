import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import bot_token

dp = Dispatcher()
bot = Bot(token=bot_token)


async def bot_send_message_if_user_offline(message_owner_name: str, text: str, user_tlg_id: int or str) -> None:
    await bot.send_message(chat_id=user_tlg_id, text=f"{message_owner_name} отправил(а) вам сообщение.\n\n{text}")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


async def main() -> None:
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
