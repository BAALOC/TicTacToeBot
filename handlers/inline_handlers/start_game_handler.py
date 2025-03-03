from handlers.game_handlers.game_utils import create_game_board, send_game_message
from loader import bot
from telebot import types
import random
from config import GAMES_DICT
from utils import logger


@bot.callback_query_handler(func=lambda call: call.data.startswith('gamemode#'))
def handle_start_game(call: types.CallbackQuery) -> None:
    """Обрабатывает запрос на начало игры."""
    try:
        bot.answer_callback_query(call.id, 'Запуск игры...')
        
        game_id = call.from_user.id
        game_mode = call.data.split("#")[1]
        invite_link = f'https://t.me/TicTacToeBaalocBot?start={game_id}'
        
        message_text = (
            f'🎮 Отлично! Давай начнем игру! Режим игры: {game_mode}\n\n'
            f'Перешли это сообщение другу, с которым хочешь сыграть:\n\n{invite_link}\n\n'
            '👆 Когда твой друг перейдет по этой ссылке, вы сможете начать игру!'
        )
        bot.send_message(call.from_user.id, message_text)
        
        size = int(game_mode.split("x")[0])
        GAMES_DICT[game_id] = {
            'size': size,
            'player1': {
                'id': call.from_user.id,
                'username': call.from_user.username,
                'symbol': random.choice(['❌', '⭕']),
            },
            'player2': None,
            'board': create_game_board(size, game_id),
            'current_turn': None
        }
        
        logger.info(f'Игра {game_id} создана. Размер: {size}x{size}. Игрок 1: {call.from_user.username}')

    except Exception as e:
        logger.error(f'Ошибка в handle_start_game: {e}', exc_info=True)
        bot.answer_callback_query(call.id, 'Произошла ошибка при выполнении команды. Попробуй позже')


@bot.callback_query_handler(func=lambda call: call.data == 'bot_start_game')
def handle_bot_start_game(call: types.CallbackQuery) -> None:
    """Обрабатывает запрос на начало игры с ботом."""
    try:
        bot.answer_callback_query(call.id, 'Запуск игры...')
        bot.send_message(call.from_user.id, 'Игра с ботом началась!')

        game_id = call.from_user.id
        player_symbol = random.choice(['❌', '⭕'])
        bot_symbol = '❌' if player_symbol == '⭕' else '⭕'
        
        GAMES_DICT[game_id] = {
            'size': 3,
            'player1': {
                'id': call.from_user.id,
                'username': call.from_user.username,
                'symbol': player_symbol,
            },
            'player2': {
                'id': 'bot',
                'username': 'Ботик',
                'symbol': bot_symbol,
            },
            'board': create_game_board(3, game_id),
            'current_turn': call.from_user.id
        }

        logger.info(f'Игра {game_id} создана. Размер: 3x3. Игрок 1: {call.from_user.username}, Игрок 2: Ботик')
        send_game_message(game_id)

    except KeyError:
        logger.warning(f'Игра {game_id} не найдена')
        bot.answer_callback_query(call.id, 'Игра не найдена')
    except Exception as e:
        logger.error(f'Ошибка в handle_bot_start_game: {e}', exc_info=True)
        bot.answer_callback_query(call.id, 'Произошла ошибка при выполнении команды. Попробуй позже')