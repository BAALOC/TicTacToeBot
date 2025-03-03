from loader import bot
from telebot import types

from utils import logger
from config import COMMANDS_DESCRIPTION
from keyboards import get_main_menu


@bot.message_handler(commands=['help'])
def help_handler(message: types.Message) -> None:
    try:
        logger.info(f'Пользователь {message.from_user.username}: /help')

        
        commands_info = '\n'.join(f'/{command} - {info}' for command, info in COMMANDS_DESCRIPTION)
        message_text = f'📄 Доступные команды:\n{commands_info}'
        bot.send_message(message.chat.id, message_text)

    except Exception as e:
        logger.error(f'Ошибка в /help: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')




