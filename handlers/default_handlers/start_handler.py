from loader import bot
from telebot import types

from utils import logger    
from database import User
from keyboards import get_main_menu
from config import COMMANDS_DESCRIPTION 


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message) -> None:
    try:
        logger.info(f'Пользователь {message.from_user.username}: /start')
        command_text = message.text.split()
        
        if len(command_text) > 1:
            bot.send_message(message.chat.id, '👋 Привет, Макар!')
        else:
            commands_info = '\n'.join(f'/{command} - {info}' for command, info in COMMANDS_DESCRIPTION)
            message_text = f'👋 Привет, Макар!\n\n📄 Доступные команды:\n{commands_info}\n\nНажми на кнопку ниже, чтобы начать! 🚀'
            bot.send_message(message.chat.id, message_text, reply_markup=get_main_menu())

            _, created = User.get_or_create(
                    user_id=message.from_user.id,
                    defaults={'username': message.from_user.username}
                )
            if created:
                logger.info(f'Новый пользователь: {message.from_user.username}')


    except Exception as e:
        logger.error(f'Ошибка в /start: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')

