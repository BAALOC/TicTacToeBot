from loader import bot
from telebot import types
from typing import List


def get_gameboard(game_id: int) -> types.InlineKeyboardMarkup:
    """Создает игровую доску для игры."""
    gameboard = types.InlineKeyboardMarkup(row_width=3)
    board = create_gameboard(game_id)
    for row in board:
        gameboard.row(*row)
    return gameboard


def create_gameboard(game_id: str) -> List[List[types.InlineKeyboardButton]]:
    """Создает кнопки для игровой доски."""
    gameboard = []

    for x in range(3):
        row = []
        for y in range(3):
            button = types.InlineKeyboardButton(
                text='⬜',
                callback_data=f'game#{game_id}#{x}#{y}'
            )
            row.append(button)
        gameboard.append(row)
    return gameboard

