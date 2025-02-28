from loader import bot
from telebot import types
from utils import logger
from config import GAMES_DICT


def handle_join_game(message: types.Message, game_id: int) -> None:
    """Обрабатывает запрос на вступление в игру."""
    try:    
        player1_id = GAMES_DICT[game_id]['player1_id']
        player2_id = message.from_user.id
        GAMES_DICT[game_id]['player2_id'] = player2_id

        player1_username = GAMES_DICT[game_id]['player1_username']
        player2_username = message.from_user.username
        GAMES_DICT[game_id]['player2_username'] = player2_username

        bot.send_message(player1_id, f'{player2_username} присоединился к игре! ✅')
        bot.send_message(player2_id, f'{player1_username} присоединился к игре! ✅')
        
    except Exception as e:
        logger.error(f'Ошибка в handle_join_game: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')

