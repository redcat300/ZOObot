import asyncio
import aiohttp
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.utils.formatting import (
   Bold, as_list, as_marked_section
)
from token_data import TOKEN
from quiz_handlers import router

dp = Dispatcher()
dp.include_router(router)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
       kb = [
          [
              types.KeyboardButton(text="Начать викторину"),
              types.KeyboardButton(text="О нас"),
          ],
       ]
       keyboard = types.ReplyKeyboardMarkup(
           keyboard=kb,
           resize_keyboard=True,
       )
       await message.answer(f"Привет! Это бот викторины. Нажми ""Начать викторину"", чтобы начать викторину.", reply_markup=keyboard)


@dp.message(F.text.lower() == "о нас")
async def description(message: types.Message):
    await message.answer("Московский зоопарк — один из старейших зоопарков Европы с уникальной коллекцией животных и профессиональным сообществом."
                         "Важная задача зоопарка — вносить вклад в сохранение биоразнообразия планеты."
                         "При нынешних темпах развития цивилизации к 2050 году могут погибнуть около 10 000 биологических видов. Московский зоопарк пытается сохранить их."
                         "«Возьми животное под опеку» («Клуб друзей») — это одна из программ, помогающих зоопарку заботиться о его обитателях."
                         " Программа позволяет с помощью пожертвования на любую сумму внести свой вклад в развитие зоопарка и сохранение биоразнообразия планеты. ")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


