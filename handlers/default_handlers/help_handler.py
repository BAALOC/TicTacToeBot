from telebot import types
from loader import bot
from utils import logger
from config import COMMANDS_DESCRIPTION


@bot.message_handler(commands=['help'])
def help_handler(message: types.Message) -> None:
    """Обрабатывает команду /help."""
    try:
        logger.info(f'Пользователь {message.from_user.username}: /help')
        
        commands_info = '\n'.join(f'/{command} - {info}' for command, info in COMMANDS_DESCRIPTION)
        message_text = f'📄 Доступные команды:\n{commands_info}'
        
        bot.send_message(message.chat.id, message_text)

    except Exception as e:
        logger.error(f'Ошибка в /help: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')




