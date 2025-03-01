from telebot import types

from loader import bot
from utils import logger
from config import GAMES_DICT
from keyboards import get_main_menu
from handlers.game_handlers.game_utils import send_game_message


@bot.callback_query_handler(func=lambda call: call.data.startswith('game#'))
def handle_gameboard_callback(call: types.CallbackQuery) -> None:
    """Обрабатывает нажатие на клетку игрового поля."""
    try:
        game_id, x, y = call.data.split('#')[1:]
        game_id = int(game_id)
        x = int(x)
        y = int(y)

        if not validate_move(game_id, x, y, call):
            return
        bot.answer_callback_query(call.id, 'Кнопка нажата')
        logger.info(f'Игрок {call.from_user.username} нажал на клетку ({x}, {y}) в игре {game_id}.')

        current_turn_id = GAMES_DICT[game_id]['current_turn']
        player1_id = GAMES_DICT[game_id]['player1']['id']
        player2_id = GAMES_DICT[game_id]['player2']['id']

        current_symbol = get_current_symbol(game_id, current_turn_id)
        GAMES_DICT[game_id]['board'][x][y].text = current_symbol
        GAMES_DICT[game_id]['current_turn'] = player2_id if current_turn_id == player1_id else player1_id

        send_game_message(game_id)
        handle_game_result(game_id, current_symbol)

    except KeyError:
        logger.warning(f'Игра {game_id} не найдена')
        bot.answer_callback_query(call.id, 'Игра не найдена')
    except Exception as e:
        logger.error(f'Ошибка в handle_gameboard_callback: {e}', exc_info=True)
        bot.send_message(call.from_user.id, 'Произошла ошибка при выполнении команды. Попробуй позже')

def get_current_symbol(game_id: int, current_turn_id: int) -> str:
    """Возвращает символ текущего игрока."""
    player1_id = GAMES_DICT[game_id]['player1']['id']
    player1_symbol = GAMES_DICT[game_id]['player1']['symbol']
    player2_symbol = GAMES_DICT[game_id]['player2']['symbol']
    
    return player1_symbol if current_turn_id == player1_id else player2_symbol

def update_board(game_id: int, x: int, y: int, symbol: str) -> None:
    """Обновляет игровое поле с новым символом."""
    GAMES_DICT[game_id]['board'][x][y].text = symbol
    
    current_player_id = GAMES_DICT[game_id]['current_turn']
    if current_player_id == GAMES_DICT[game_id]['player1']['id']:   
        GAMES_DICT[game_id]['current_turn'] = GAMES_DICT[game_id]['player2']['id']
    else:
        GAMES_DICT[game_id]['current_turn'] = GAMES_DICT[game_id]['player1']['id']

def handle_game_result(game_id: int, current_symbol: str) -> None:
    """Обрабатывает результат игры и отправляет сообщение игрокам."""
    player_ids = [
        GAMES_DICT[game_id]['player1']['id'],
        GAMES_DICT[game_id]['player2']['id']
    ]

    result = check_game_end(game_id)
    if result == 'draw':
        logger.info(f'Игра {game_id} закончилась вничью')
        message_text = '🤝 Игра закончилась вничью!'
    elif result:
        logger.info(f'Игрок {current_symbol} выиграл игру {game_id}')
        message_text = f'🎉 Игра закончена! Победил игрок: {current_symbol}'
    
    if result:
        for player_id in player_ids:
            bot.send_message(player_id, message_text, reply_markup=get_main_menu())
        GAMES_DICT.pop(game_id)

def check_game_end(game_id: int) -> bool | str:
    """Проверяет, закончена ли игра."""
    board = GAMES_DICT[game_id]['board']
    size = GAMES_DICT[game_id]['size']
    
    for i in range(size):
        if all(board[i][j].text == '❌' for j in range(size)) or all(board[j][i].text == '❌' for j in range(size)):
            return True
        if all(board[i][j].text == '⭕' for j in range(size)) or all(board[j][i].text == '⭕' for j in range(size)):
            return True

    if all(board[i][i].text == '❌' for i in range(size)) or all(board[i][size - 1 - i].text == '❌' for i in range(size)):
        return True
    if all(board[i][i].text == '⭕' for i in range(size)) or all(board[i][size - 1 - i].text == '⭕' for i in range(size)):
        return True

    if all(cell.text != '⬜' for row in board for cell in row):
        return 'draw'  

    return False

def validate_move(game_id: int, x: int, y: int, call: types.CallbackQuery) -> bool:
    """Проверяет, является ли ход допустимым."""
    button_text = GAMES_DICT[game_id]['board'][x][y].text
    current_turn = GAMES_DICT[game_id]['current_turn']

    if button_text != '⬜':
        logger.warning(f'Клетка ({x}, {y}) уже занята в игре {game_id}')
        bot.answer_callback_query(call.id, 'Клетка уже занята')
        return False

    if current_turn != call.from_user.id:
        logger.info(f'Игрок {call.from_user.username} попытался сделать ход не в свой ход в игре {game_id}')
        bot.answer_callback_query(call.id, 'Сейчас не твой ход')
        return False

    return True