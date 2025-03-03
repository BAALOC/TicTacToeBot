from loader import bot
from config import GAMES_DICT
from keyboards import get_gameboard, get_main_menu
from utils import logger
from telebot import types


def create_game_message(game_id: int, player_id: int) -> str:
    """Создает сообщение для игрока, показывающее чья очередь и символ игрока."""
    game_data = GAMES_DICT[game_id]
    
    if player_id == game_data['player1']['id']:
        player_symbol = game_data['player1']['symbol']
    else:
        player_symbol = game_data['player2']['symbol']
    
    if game_data['current_turn'] == player_id:
        current_turn_message = 'Сейчас твоя очередь, сделай свой ход! 🚀'
    else:
        current_turn_message = 'Сейчас не твоя очередь, жди хода! ⏳'
    
    return f'Твой символ: {player_symbol}. {current_turn_message}'


def send_game_message(game_id: int) -> None:
    """Отправляет сообщение игрокам с обновленным игровым полем или боту."""
    game_data = GAMES_DICT[game_id]
    player1_id = game_data['player1']['id']
    player2_id = game_data['player2']['id']
    board = get_gameboard(game_id)
    
    if player2_id != 'bot':
        for i, player_id in enumerate([player1_id, player2_id], start=1):
            message_text = create_game_message(game_id, player_id)
            message_key = f'message_{i}'

            if game_data.get(message_key):
                bot.edit_message_text(message_text, player_id, game_data[message_key].id, reply_markup=board)
            else:
                sent_message = bot.send_message(player_id, message_text, reply_markup=board)
                game_data[message_key] = sent_message

    else:
        message_text = create_game_message(game_id, player1_id)
        message_key = 'message_1'

        if game_data.get(message_key):
            bot.edit_message_text(message_text, player1_id, game_data[message_key].id, reply_markup=board)
        else:
            sent_message = bot.send_message(player1_id, message_text, reply_markup=board)
            game_data[message_key] = sent_message


def handle_game_result(game_id: int) -> None:
    """Обрабатывает результат игры и отправляет сообщение игрокам."""
    player_ids = [GAMES_DICT[game_id]['player1']['id'], GAMES_DICT[game_id]['player2']['id']]
    result, current_symbol = check_game_end(game_id)
    winner_username = (
        GAMES_DICT[game_id]['player2']['username'] 
        if current_symbol == GAMES_DICT[game_id]['player2']['symbol'] 
        else GAMES_DICT[game_id]['player1']['username']
    )

    if result == 'draw':
        message_text = '🤝 Игра закончилась ничьей!'
        logger.info(f'Игра {game_id} закончилась ничьей')
    elif result:
        message_text = f'🎉 Игра закончена! Победил игрок: {winner_username} ({current_symbol})'
        logger.info(f'Игрок {winner_username} выиграл игру {game_id}')
    
    if result:
        if GAMES_DICT[game_id]['player2']['id'] != 'bot':
            for player_id in player_ids:
                bot.send_message(player_id, message_text, reply_markup=get_main_menu())
        else:
            bot.send_message(GAMES_DICT[game_id]['player1']['id'], message_text, reply_markup=get_main_menu())
        GAMES_DICT.pop(game_id) 


def check_game_end(game_id: int) -> tuple[bool, str]:
    """Проверяет, закончена ли игра."""
    board = GAMES_DICT[game_id]['board']
    size = GAMES_DICT[game_id]['size']
    
    for i in range(size):
        if all(board[i][j].text == '❌' for j in range(size)) or all(board[j][i].text == '❌' for j in range(size)):
            return True, '❌'
        if all(board[i][j].text == '⭕' for j in range(size)) or all(board[j][i].text == '⭕' for j in range(size)):
            return True, '⭕'

    if all(board[i][i].text == '❌' for i in range(size)) or all(board[i][size - 1 - i].text == '❌' for i in range(size)):
        return True, '❌'
    if all(board[i][i].text == '⭕' for i in range(size)) or all(board[i][size - 1 - i].text == '⭕' for i in range(size)):
        return True, '⭕'

    if all(cell.text != '⬜' for row in board for cell in row):
        return 'draw', None

    return False, None


def update_board(game_id: int, x: int, y: int, symbol: str) -> None:
    """Обновляет игровое поле с новым символом для игры с ботом и с другом."""
    GAMES_DICT[game_id]['board'][x][y].text = symbol
    
    current_player_id = GAMES_DICT[game_id]['current_turn']
    if current_player_id == GAMES_DICT[game_id]['player1']['id']:   
        GAMES_DICT[game_id]['current_turn'] = GAMES_DICT[game_id]['player2']['id']
    else:
        GAMES_DICT[game_id]['current_turn'] = GAMES_DICT[game_id]['player1']['id']


def validate_move(game_id: int, x: int, y: int, call: types.CallbackQuery) -> bool:
    """Проверяет, является ли ход допустимым."""
    try:
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

    except KeyError:
        logger.warning(f'Игрок {call.from_user.username} пытался сделать ход в несуществующей игре: {game_id}')
        bot.answer_callback_query(call.id, 'Игра не найдена')
        return False
    
    return True


def create_game_board(size: int, game_id: int) -> list:
    """Создает игровое поле."""
    return [
        [types.InlineKeyboardButton(text='⬜', callback_data=f'game#{game_id}#{x}#{y}') for y in range(size)]
        for x in range(size)
    ]