from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

answ = dict()

# кнопки посилань
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton1 = InlineKeyboardButton(text='Посилання1', url='https://youtube.com')
urlButton2 = InlineKeyboardButton(text='Посилання2', url='https://google.com')
url_button3_5 = [
    InlineKeyboardButton(text='Посилання3', url='https://google.com'),
    InlineKeyboardButton(text='Посилання4', url='https://google.com'),
    InlineKeyboardButton(text='Посилання5', url='https://google.com')
]
urlButton6 = InlineKeyboardButton(text='Посилання6', url='https://google.com')
urlkb.add(urlButton1, urlButton2).row(*url_button3_5).insert(urlButton6)


@dp.message_handler(commands='Посилання')
async def url_command(message: types.Message):
    await message.answer('Посилання', reply_markup=urlkb)


inline_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Like', callback_data='like_1'),
                                                  InlineKeyboardButton(text='dislike', callback_data='like_-1'))


@dp.message_handler(commands='test')
async def test_command(message: types.Message):
    await message.answer('За деплой відео', reply_markup=inline_kb)


@dp.callback_query_handlers(Text(startswith='like_'))
async def www_call(callback: types.CallbackQuery):
    result = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = result
        await callback.answer('Ви проголосували')
    else:
        await callback.answer('Ви вже голосували', show_alert=True)


executor.start_polling(dp, skip_updates=True)
