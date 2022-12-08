from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

# Кнопки клавіатури клієнта
button_1 = KeyboardButton('/Режим_роботи')
button_2 = KeyboardButton('/Локація')
button_3 = KeyboardButton('/Меню')
button_4 = KeyboardButton('Надати номер', request_contact=True)
button_5 = KeyboardButton('Надати локацію', request_location=True)

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(button_1, button_2).row(button_3).row(button_4, button_5)
