import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram import Router
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.filters import CommandStart
from aiogram.types import ChatMemberUpdated
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger  # https://github.com/Delgan/loguru

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
print(TOKEN)

dp = Dispatcher()


def menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура главного меню"""
    rows = [
        [InlineKeyboardButton(text='Перейти в канал', url='https://t.me/alpha_dom_vr')],
    ]
    main_menu_key = InlineKeyboardMarkup(inline_keyboard=rows)
    return main_menu_key


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    message_text = (f"Здравствуй, {message.from_user.first_name} 🫶! \n\n"

                    "С 12 июля по 4 августа 2024 года мы проводим конкурс. Победители получат возможность тестового "
                    "проживания в нашем доме на территории выставки Open Village24.\n\n"

                    "Для участия в конкурсе достаточно подписаться на официальный telegram-канал компании. Результаты "
                    "будут опубликованы здесь.\n\n"

                    "Прочувствуй загородную жизнь с DRHouse 🤍")

    await message.answer(message_text, reply_markup=menu_keyboard())


new_member_router = Router()


@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    """
    Пользователь вступил в группу
    IS_NOT_MEMBER >> IS_MEMBER - новый участник
    IS_MEMBER >> IS_NOT_MEMBER - покинул группу участник группы
    """
    logger.info(f'Пользователь: Имя - {event.new_chat_member.user.first_name} {event.new_chat_member.user.last_name} '
                f'username - {event.new_chat_member.user.username} id - {event.new_chat_member.user.id} '
                f'вступил в группу.')


@dp.message(F.new_chat_members)
async def new_chat_member(message: types.Message):
    """
    Пользователь вступил в группу
    ContentType = new_chat_members (https://docs.aiogram.dev/en/v3.1.1/api/enums/content_type.html)
    """
    await message.delete()  # Удаляем системное сообщение о новом участнике группы
    logger.info(f'Пользователь: Имя  -  {message.from_user.first_name}  {message.from_user.last_name}  ')

    message_text = (f"Здравствуй, {message.from_user.first_name} 🫶! \n\n"

                    "С 12 июля по 4 августа 2024 года мы проводим конкурс. Победители получат возможность тестового "
                    "проживания в нашем доме на территории выставки Open Village24.\n\n"

                    "Для участия в конкурсе достаточно подписаться на официальный telegram-канал компании. Результаты "
                    "будут опубликованы здесь.\n\n"

                    "Прочувствуй загородную жизнь с DRHouse 🤍")

    await message.answer(message_text, reply_markup=menu_keyboard())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
