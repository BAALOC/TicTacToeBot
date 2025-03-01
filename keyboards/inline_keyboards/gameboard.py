from telebot import types
from config import GAMES_DICT


def get_gameboard(game_id: int) -> types.InlineKeyboardMarkup:
    """Создает игровую доску для игры."""
    gameboard = types.InlineKeyboardMarkup(row_width=3)
    board = GAMES_DICT[game_id]['board']
    for row in board:
        gameboard.row(*row)
    return gameboard
