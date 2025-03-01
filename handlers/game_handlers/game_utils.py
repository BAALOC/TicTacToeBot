from telebot import types

from loader import bot
from config import GAMES_DICT
from keyboards import get_gameboard
from utils import logger


def create_game_message(game_id: int, player_id: int) -> str:
    """Создает сообщение для игрока, показывающее чья очередь и символ игрока."""
    game_data = GAMES_DICT[game_id]
    player1_symbol = game_data['player1']['symbol']
    player2_symbol = game_data['player2']['symbol']
    current_turn = game_data['current_turn']

    pointer_symbol = player1_symbol if player_id == game_data['player1']['id'] else player2_symbol
    current_turn_message = (
        'Сейчас твоя очередь, сделай свой ход! 🚀' if current_turn == player_id 
        else 'Сейчас не твоя очередь, жди хода! ⏳'
    )

    return f'Твой символ: {pointer_symbol}. {current_turn_message}'


def send_game_message(game_id: int) -> None:
    """Отправляет сообщение игрокам с обновленным игровым полем."""
    game_data = GAMES_DICT[game_id]
    player1_id = game_data['player1']['id']
    player2_id = game_data['player2']['id']
    board = get_gameboard(game_id)

    for i, player_id in enumerate([player1_id, player2_id], start=1):
        message_text = create_game_message(game_id, player_id)
        message_key = f'message_{i}'

        if game_data.get(message_key):
            bot.edit_message_text(message_text, player_id, game_data[message_key].id, reply_markup=board)
        else:
            sent_message = bot.send_message(player_id, message_text, reply_markup=board)
            game_data[message_key] = sent_message
