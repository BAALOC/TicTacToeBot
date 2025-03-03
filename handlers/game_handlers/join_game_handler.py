from telebot import types
from loader import bot
from utils import logger
from config import GAMES_DICT
from handlers.game_handlers.game_utils import send_game_message
import random
from keyboards import get_main_menu


def handle_join_game(message: types.Message, game_id: int) -> None:
    """Обрабатывает запрос на вступление в игру."""
    try:
        if not validate_join_game(message, game_id):
            return

        player_symbol = '⭕' if GAMES_DICT[game_id]['player1']['symbol'] == '❌' else '❌'
        player = {
            'id': message.from_user.id,
            'username': message.from_user.username,
            'symbol': player_symbol,
        }

        GAMES_DICT[game_id]['player2'] = player
        GAMES_DICT[game_id]['current_turn'] = random.choice([GAMES_DICT[game_id]['player1']['id'], message.from_user.id])

        logger.info(f'Игрок {message.from_user.username} присоединился к игре {game_id}. '
                    f'Игрок 1: {GAMES_DICT[game_id]["player1"]["username"]} '
                    f'Игрок 2: {player["username"]}')
        send_game_message(game_id)

    except Exception as e:
        logger.error(f'Ошибка в handle_join_game: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')


def validate_join_game(message: types.Message, game_id: int) -> bool:
    if game_id not in GAMES_DICT:
        logger.warning(f'Игрок {message.from_user.username} пытался присоединиться к несуществующей игре: {game_id}')
        bot.send_message(message.chat.id, 'Игра не найдена. Проверь ID игры и попробуй снова', reply_markup=get_main_menu())
        return False

    if GAMES_DICT[game_id]['player2'] is not None:
        logger.warning(f'Игрок {message.from_user.username} пытался присоединиться к заполненной игре: {game_id}')
        bot.send_message(message.chat.id, 'Игра уже заполнена. Ты не можешь присоединиться к ней', reply_markup=get_main_menu())
        return False

    if message.from_user.id == GAMES_DICT[game_id]['player1']['id']:
        logger.warning(f'Игрок {message.from_user.username} пытался присоединиться к своей игре: {game_id}')
        bot.send_message(message.chat.id, 'Ясное дело, что ты не можешь присоединиться к своей игре, гений 🤡', reply_markup=get_main_menu())
        return False

    return True
