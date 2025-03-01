from loader import bot
from telebot import types
from utils import logger
from config import GAMES_DICT
from handlers.game_handlers.game_utils import send_game_message
import random


def handle_join_game(message: types.Message, game_id: int) -> None:
    """Обрабатывает запрос на вступление в игру."""
    try:
        if game_id not in GAMES_DICT:
            logger.warning(f'Игрок {message.from_user.username} пытался присоединиться к несуществующей игре: {game_id}')
            bot.send_message(message.chat.id, 'Игра не найдена. Проверь ID игры и попробуй снова')
            return

        if GAMES_DICT[game_id]['player2'] is not None:
            logger.warning(f'Игрок {message.from_user.username} пытался присоединиться к заполненной игре: {game_id}')
            bot.send_message(message.chat.id, 'Игра уже заполнена. Ты не можешь присоединиться к ней')
            return
        
        if GAMES_DICT[game_id]['player1']['id'] == message.from_user.id:
            logger.warning(f'Игрок {message.from_user.username} пытался присоединиться к своей игре: {game_id}')
            bot.send_message(message.chat.id, 'Ты не можешь присоединиться к своей игре, гений ♿️')
            return  
        
        player = {
            'id': message.from_user.id,
            'username':  message.from_user.username,
            'symbol':  '⭕' if GAMES_DICT[game_id]['player1']['symbol'] == '❌' else '❌',
        }
        GAMES_DICT[game_id]['player2'] = player
        GAMES_DICT[game_id]['current_turn'] = random.choice([GAMES_DICT[game_id]['player1']['id'], message.from_user.id])

        player1_id = GAMES_DICT[game_id]['player1']['username']
        player2_id = GAMES_DICT[game_id]['player2']['username']
        logger.info(f'Игрок {message.from_user.username} присоединился к игре {game_id}. 1) Игрок 1: {player1_id} 2) Игрок 2: {player2_id}')
        send_game_message(game_id)

    except Exception as e:
        logger.error(f'Ошибка в handle_join_game: {e}', exc_info=True)
        bot.send_message(message.chat.id, 'Произошла ошибка при выполнении команды. Попробуй позже')

