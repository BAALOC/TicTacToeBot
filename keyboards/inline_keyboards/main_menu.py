from telebot import types


def get_main_menu() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Играть с другом 🎮', callback_data='start_game'))
    keyboard.add(types.InlineKeyboardButton(text='Играть с ботом 🤖', callback_data='bot_start_game'))
    return keyboard
