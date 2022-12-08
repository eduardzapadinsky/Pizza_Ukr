from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import keyboard_client
from data_bases.sqlite_db import sql_read


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Смачного', reply_markup=keyboard_client)
        await message.delete()
    except:
        await message.reply('Спілкування з ботом через ОС, напишіть йому:\nhttps://t.me/Pizza_UkrBot')


# @dp.message_handler(commands=['Режим_роботи'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Пн-Чт 9:00-20:00, Пт-Нд 9:00-22:00")


# @dp.message_handler(commands=['Локація'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, "вул. Піцци, 2")#, reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message: types.Message):
    await sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_роботи'])
    dp.register_message_handler(pizza_place_command, commands=['Локація'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])
