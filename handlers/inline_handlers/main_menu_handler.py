from telebot import types
from loader import bot
from utils import logger
from config import GAMES_DICT
from keyboards import get_game_choice_keyboard
import random


@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def handle_main_menu(call: types.CallbackQuery) -> None:
    """Обрабатывает запрос на начало игры из главного меню."""
    try:
        bot.send_message(call.from_user.id, 'Выбери режим игры 👇:', reply_markup=get_game_choice_keyboard())
    except Exception as e:
        logger.error(f'Ошибка в handle_main_menu: {e}', exc_info=True)
        bot.answer_callback_query(call.id, 'Произошла ошибка при выполнении команды. Попробуй позже')


@bot.callback_query_handler(func=lambda call: call.data.startswith('gamemode#'))
def handle_start_game(call: types.CallbackQuery) -> None:
    try:
        """Обрабатывает запрос на начало игры."""
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
        player1_id = call.from_user.id
        GAMES_DICT[game_id] = {
            'size': size,
            'player1': {
                'id': player1_id,
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


def create_game_board(size: int, game_id: int) -> list:
    """Создает игровое поле."""
    return [
        [types.InlineKeyboardButton(text='⬜', callback_data=f'game#{game_id}#{x}#{y}') for y in range(size)]
        for x in range(size)
    ]