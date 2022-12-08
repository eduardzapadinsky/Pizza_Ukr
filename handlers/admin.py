from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import data_bases.sqlite_db
from data_bases.sqlite_db import sql_add_command
from keyboards.admin_kb import button_case_admin

from create_bot import dp, bot

ID = None


class FsmAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    """Отримуємо ID модератора"""
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Вкажіть команду", reply_markup=button_case_admin)
    await message.delete()


# @dp.message_handler(commands='Завантажити', state=None)
async def cm_start(message: types.Message):
    """Початок діалогу завантаження нового пункту меню"""
    if message.from_user.id == ID:
        await FsmAdmin.photo.set()
        await message.reply('Завантаж фото')


# @dp.message_handler(state="*", commands="Відміна")
# @dp.message_handler(Text(equals='відміна', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """Вихід зі стану"""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("OK")


# @dp.message_handler(content_types=['photo'], state=FsmAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    """Зберігаємо 1 відповідь в dict"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FsmAdmin.next()
        await message.reply('Тепер введіть назву')


# @dp.message_handler(state=FsmAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    """Зберігаємо 2 відповідь в dict"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FsmAdmin.next()
        await message.reply('Тепер опис')


# @dp.message_handler(state=FsmAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    """Зберігаємо 3 відповідь в dict"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FsmAdmin.next()
        await message.reply('Тепер вкажіть ціну')


# @dp.message_handler(state=FsmAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    """Зберігаємо 4 (останню) відповідь в dict"""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sql_add_command(state)
        await state.finish()


async def del_callback_run(callback_query: types.CallbackQuery):
    await data_bases.sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} видалена", show_alert=True)


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await data_bases.sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОпис: {ret[2]}\nЦіна {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^',
                                   reply_markup=types.InlineKeyboardMarkup().
                                   add(types.InlineKeyboardButton(f'Видалити {ret[1]}', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp: Dispatcher):
    """Реєструємо хендлери"""
    dp.register_message_handler(cm_start, commands=['Завантажити'], state=None)
    dp.register_message_handler(cancel_handler, Text(equals='відміна', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FsmAdmin.photo)
    dp.register_message_handler(load_name, state=FsmAdmin.name)
    dp.register_message_handler(load_description, state=FsmAdmin.description)
    dp.register_message_handler(load_price, state=FsmAdmin.price)
    dp.register_message_handler(cancel_handler, state="*", commands="Відміна")

    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands='Видалити')
