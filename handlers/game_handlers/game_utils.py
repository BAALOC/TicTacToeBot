from loader import bot
from telebot import types
from config import GAMES_DICT
from keyboards import get_gameboard


def create_game_message(game_id: int, player_id: int) -> str:
    """Создает сообщение для игрока, показывающее чья очередь и символ игрока."""
    player1_symbol = GAMES_DICT[game_id]['player1']['symbol']
    player2_symbol = GAMES_DICT[game_id]['player2']['symbol']
    current_turn = GAMES_DICT[game_id]['current_turn']

    if player_id == GAMES_DICT[game_id]['player1']['id']:
        pointer_symbol = player1_symbol
    else:
        pointer_symbol = player2_symbol

    if current_turn == player_id:
        current_turn_message = 'Сейчас твоя очередь, сделай свой ход! 🚀'
    else:
        current_turn_message = 'Сейчас не твоя очередь, жди хода! ⏳'

    message_text = f'Твой символ: {pointer_symbol}. {current_turn_message}'
    return message_text


def send_game_message(game_id: int, sent_message: types.Message | None = None) -> None:
    """Отправляет сообщение игрокам с обновленным игровым полем."""
    player1_id = GAMES_DICT[game_id]['player1']['id']
    player2_id = GAMES_DICT[game_id]['player2']['id']
    board = get_gameboard(game_id)

    if not all(GAMES_DICT[game_id].get(f'message_{i}') for i in [1, 2]):
        for i, player_id in enumerate([player1_id, player2_id], 1):      
            message_text = create_game_message(game_id, player_id)
            sent_message = bot.send_message(player_id, message_text, reply_markup=board)
            GAMES_DICT[game_id][f'message_{i}'] = sent_message
    else:
        for i, player_id in enumerate([player1_id, player2_id], 1):
            message_text = create_game_message(game_id, player_id)
            bot.edit_message_text(message_text, player_id, GAMES_DICT[game_id][f'message_{i}'].id, reply_markup=board)

