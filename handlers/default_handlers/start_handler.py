from loader import bot
from telebot import types
from utils import logger
from database import User
from keyboards import get_main_menu
from config import COMMANDS_DESCRIPTION 
from handlers.game_handlers.join_game_handler import handle_join_game

@bot.message_handler(commands=['start'])
def start_handler(message: types.Message) -> None:
    """Обрабатывает команду /start."""
    try:
        username = message.from_user.username if message.from_user.username else f'user_{message.from_user.id}'
        
        _, created = User.get_or_create(
                user_id=message.from_user.id,
                defaults={'username': username}
            )
        if created:
            logger.info(f'Новый пользователь: {username}')
            
        command_text = message.text.split()   
        if len(command_text) > 1:
            handle_join_game(message, game_id=int(command_text[1]))
        else:
            logger.info(f'Пользователь {username}: /start')
            commands_info = '\n'.join(f'/{command} - {info}' for command, info in COMMANDS_DESCRIPTION)
            message_text = (
                f'👋 Привет, {message.from_user.full_name}!\n\n'
                f'📄 Доступные команды:\n{commands_info}\n\n'
                'Нажми на кнопку ниже, чтобы начать! 🚀'
            )
            bot.send_message(message.chat.id, message_text, reply_markup=get_main_menu())

    except Exception as e:
        logger.error(f'Ошибка в /start: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')

