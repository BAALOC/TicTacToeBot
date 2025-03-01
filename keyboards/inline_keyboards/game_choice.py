from telebot import types


def get_game_choice_keyboard() -> types.InlineKeyboardMarkup:
    """Возвращает клавиатуру для выбора игры."""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Играть в 3x3 🎮', callback_data='gamemode#3x3')
    button2 = types.InlineKeyboardButton(text='Играть в 4x4 🎲', callback_data='gamemode#4x4')
    button3 = types.InlineKeyboardButton(text='Играть в 5x5 🕹️', callback_data='gamemode#5x5')
    keyboard.add(button1, button2, button3)
    return keyboard
