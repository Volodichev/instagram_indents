import asyncio
import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import exceptions, executor

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided. Terminated.")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.debug(f"Target [ID:{user_id}]: success")
        return True
    return False


async def main_logic(text):
    """
    Editing text
    """
    basetext = text.encode().decode('utf-8')
    if basetext:
        strings = basetext.split('\n')
        text_list = list()
        for string in strings:
            if string == '':
                text_list.append('⠀')
            else:
                text_list.append(string.strip())

        text = '\n'.join(text_list)

    return text


@dp.message_handler()
async def text_indents_handler(message: types.Message):
    """
    Text indents handler
    """
    chat_id = message.chat.id
    text = message.text

    text = await main_logic(text=text)
    await send_message(chat_id, text)


@dp.message_handler(CommandStart())
async def command_start_handler(message: types.Message):
    """
    Start message handler
    """

    name = message.from_user.full_name
    en_name = name
    if not name:
        name = 'мой друг'
        en_name = 'my friend'

    text = f'Добро пожаловать, {name}! \n' \
           f'Просто пришли мне текст с несколькими абзацами, ' \
           f'разделенными пустыми строками!\n' \
           f'Hello, {en_name} \njust send me text with few paragraphs'

    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp)
