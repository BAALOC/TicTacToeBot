from loader import bot
from telebot import types

from utils import logger


@bot.message_handler(commands=['help'])
def help_handler(message: types.Message) -> None:
    try:
        logger.info(f'Пользователь {message.from_user.username}: /help')

        message_text = 'Помощь'
        bot.send_message(message.chat.id, message_text)

    except Exception as e:
        logger.error(f'Ошибка в /help: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')




