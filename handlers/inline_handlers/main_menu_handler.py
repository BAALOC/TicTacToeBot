from loader import bot
from telebot import types
from utils import logger
from config import GAMES_DICT
import random


@bot.callback_query_handler(func=lambda call: call.data in ['start_game'])
def handle_main_menu(call: types.CallbackQuery) -> None:
    """Обрабатывает запрос на начало игры из главного меню."""
    try:
        if call.data == 'start_game':
            bot.answer_callback_query(call.id, 'Запуск игры...')
            
            game_id = call.from_user.id
            invite_link = f'https://t.me/TicTacToeBaalocBot?start={game_id}'
            message_text = (
                f'🎮 Отлично! Давай начнем игру!\n\n'
                f'Перешли это сообщение другу, с которым хочешь сыграть:\n\n{invite_link}\n\n'
                '👆 Когда твой друг перейдет по этой ссылке, вы сможете начать игру!'
            )
            bot.send_message(call.from_user.id, message_text)
            player1_id = call.from_user.id
            GAMES_DICT[game_id] = {
                'player1': {
                    'id': player1_id,
                    'username': call.from_user.username,
                    'symbol': random.choice(['❌', '⭕']),
                },
                'player2': None,
                'board': [[types.InlineKeyboardButton(text='⬜', callback_data=f'game#{game_id}#{x}#{y}') for y in range(3)] for x in range(3)],
                'current_turn': None
            }
            logger.info(f'Игра {game_id} создана. Игрок 1: {call.from_user.username}')

    except Exception as e:
        logger.error(f'Ошибка в handle_main_menu: {e}', exc_info=True)
        bot.answer_callback_query(call.id, 'Произошла ошибка при выполнении команды. Попробуй позже')
