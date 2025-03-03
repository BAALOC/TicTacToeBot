from telebot import types


def get_main_menu() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    
    buttons = [
        types.InlineKeyboardButton(text='Играть с другом 🎮', callback_data='start_game'),
        types.InlineKeyboardButton(text='Играть с ботом 🤖', callback_data='bot_start_game')
    ]
    
    keyboard.add(*buttons)
    
    return keyboard
