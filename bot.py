import asyncio
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.message import ContentType

from config import TOKEN

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
status = 1


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global status
    status = 1
    await message.reply("Привет!\nНапиши мне что-нибудь! Что я умею подскажет /help")


# @dp.message_handler(commands=['start', 'help', 'capslock', 'lowercase', 'echo'])

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ! Можешь с помощью комманд управлять формой ответа \n"
                        "/echo -- вернуть сообщение в первосданном виде \n"
                        "/capslock -- вернуть сообщение в верхнем регистре \n"
                        "/lowercase -- вернуть сооющение в нижнем регистре \n")

@dp.message_handler(commands=['echo'])
async def process_echo_command(message: types.Message):
    global status
    status = 1
    await message.reply("Теперь я буду просто повторять за тобой!")

@dp.message_handler(commands=['capslock'])
async def process_capslock_command(message: types.Message):
    global status
    status = 2
    await message.reply("Теперь я буду кричать!")

@dp.message_handler(commands=['lowercase'])
async def process_lowercase_command(message: types.Message):
    global status
    status = 3
    await message.reply("Теперь я буду игнорировать большие буквы как все хипстеры!")

@dp.message_handler()
async def echo_message(msg: types.Message):
    if status == 1:
        await bot.send_message(msg.from_user.id, msg.text)
    elif status == 2:
        await bot.send_message(msg.from_user.id, msg.text.upper())
    elif status == 3:
        await bot.send_message(msg.from_user.id, msg.text.lower())


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = 'Я не знаю, что с этим делать =_= \nЯ просто напомню что есть команда /help'
    await msg.reply(message_text)


if __name__ == '__main__':
    executor.start_polling(dp)