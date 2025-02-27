from telebot import types


def get_main_menu() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Играть 🎮', callback_data='start_game'))
    return keyboard
