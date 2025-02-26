from loader import bot
from telebot import types

from utils import logger    
from database import User


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message) -> None:
    try:
        logger.info(f'Пользователь {message.from_user.username}: /start')

        message_text = 'Привет'
        bot.send_message(message.chat.id, message_text)

        _, created = User.get_or_create(
                user_id=message.from_user.id,
                defaults={'username': message.from_user.username}
            )
        if created:
            logger.info(f'Новый пользователь: {message.from_user.username}')


    except Exception as e:
        logger.error(f'Ошибка в /start: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')

