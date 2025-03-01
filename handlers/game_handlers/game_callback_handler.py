from loader import bot
from telebot import types
from utils import logger
from config import GAMES_DICT
from handlers.game_handlers.game_utils import send_game_message
from keyboards import get_main_menu

@bot.callback_query_handler(func=lambda call: call.data.startswith('game#'))
def handle_gameboard_callback(call: types.CallbackQuery) -> None:
    """Обрабатывает нажатие на клетку игрового поля."""
    try:
        game_id, x, y = parse_callback_data(call.data)
        if not validate_move(game_id, x, y, call):
            return
        
        bot.answer_callback_query(call.id, 'Кнопка нажата')
        current_turn_id = GAMES_DICT[game_id]['current_turn']
        current_symbol = get_current_symbol(game_id, current_turn_id)

        update_board(game_id, x, y, current_symbol)
        logger.info(f'Игрок {call.from_user.username} сделал ход: {current_symbol} на клетке ({x}, {y}) в игре {game_id}')

        send_game_message(game_id, call.message)
        handle_game_result(game_id, current_symbol, call.from_user.id)

    except Exception as e:
        logger.error(f'Ошибка в handle_gameboard_callback: {e}', exc_info=True)
        bot.send_message(call.from_user.id, 'Произошла ошибка при выполнении команды. Попробуй позже')

def parse_callback_data(data: str) -> tuple:
    """Парсит данные из callback запроса."""
    game_id, x, y = data.split('#')[1:]
    return int(game_id), int(x), int(y)

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

def handle_game_result(game_id: int, current_symbol: str, user_id: int) -> None:
    """Обрабатывает результат игры и отправляет сообщение игроку."""
    player1_id = GAMES_DICT[game_id]['player1']['id']
    player2_id = GAMES_DICT[game_id]['player2']['id']

    result = check_game_end(game_id)
    if result == 'draw':
        logger.info(f'Игра {game_id} закончилась вничью')
        message_text = '🤝 Игра закончилась вничью!'
        for player_id in [player1_id, player2_id]:
            bot.send_message(player_id, message_text, reply_markup=get_main_menu())
            
    elif result:
        logger.info(f'Игрок {current_symbol} выиграл игру {game_id}')
        message_text = f'🎉 Игра закончена! Победил игрок: {current_symbol}'

        for player_id in [player1_id, player2_id]:
            bot.send_message(player_id, message_text, reply_markup=get_main_menu())

def validate_move(game_id: int, x: int, y: int, call: types.CallbackQuery) -> bool:
    """Проверяет, является ли ход допустимым."""
    try:
        button_text = GAMES_DICT[game_id]['board'][x][y].text
        if button_text != '⬜':
            logger.warning(f'Клетка ({x}, {y}) уже занята в игре {game_id}')
            bot.answer_callback_query(call.id, 'Клетка уже занята')
            return False

        current_turn = GAMES_DICT[game_id]['current_turn']
        if current_turn != call.from_user.id:
            logger.info(f'Игрок {call.from_user.username} попытался сделать ход не в свой ход в игре {game_id}')
            bot.answer_callback_query(call.id, 'Сейчас не твой ход')
            return False
        
    except KeyError:
        logger.warning(f'Игра {game_id} не найдена')
        bot.answer_callback_query(call.id, 'Игра не найдена')
        return False

    return True 

def check_game_end(game_id: int) -> bool:
    """Проверяет, закончена ли игра."""
    board = GAMES_DICT[game_id]['board']
    
    for row in board:
        if all(cell.text == '❌' for cell in row) or all(cell.text == '⭕' for cell in row):
            return True
    
    for col in range(3):
        if all(board[row][col].text == '❌' for row in range(3)) or all(board[row][col].text == '⭕' for row in range(3)):
            return True
    
    if board[0][0].text == board[1][1].text == board[2][2].text and board[0][0].text != '⬜':
        return True
    if board[0][2].text == board[1][1].text == board[2][0].text and board[0][2].text != '⬜':
        return True
    
    if all(cell.text != '⬜' for row in board for cell in row):
        return 'draw'  
    
    return False
