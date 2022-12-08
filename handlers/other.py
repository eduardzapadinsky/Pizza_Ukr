from aiogram import types, Dispatcher
import string
import json


# @dp.message_handler()
async def echo_send(message: types.Message):
    dirty_set = set(json.load(open('dirty.json')))
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}.intersection(
            dirty_set):
        await message.reply('Нецензурна лексика заборонена')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
