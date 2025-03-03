from telebot import types
from loader import bot
from utils import logger
from config import GAMES_DICT
from handlers.game_handlers.game_utils import send_game_message, validate_move, handle_game_result, update_board, check_game_end


@bot.callback_query_handler(func=lambda call: call.data.startswith('game#'))
def handle_gameboard_callback(call: types.CallbackQuery) -> None:
    """Обрабатывает ход игрока на игровом поле."""
    try:
        game_id, x, y = map(int, call.data.split('#')[1:])

        if not validate_move(game_id, x, y, call):
            return
        bot.answer_callback_query(call.id, 'Ход сделан')

        current_symbol = get_current_symbol(game_id, call.from_user.id)
        if GAMES_DICT[game_id]['player2']['id'] == 'bot':
            GAMES_DICT[game_id]['board'][x][y].text = current_symbol
            i, j = bot_move(game_id)
            if i is None and j is None:
                logger.info(f'Бот не смог сделать ход в игре {game_id}.')
            else:
                GAMES_DICT[game_id]['board'][i][j].text = GAMES_DICT[game_id]['player2']['symbol']
            
        else:
            update_board(game_id, x, y, current_symbol)

        send_game_message(game_id)
        handle_game_result(game_id)

    except Exception as e:
        logger.error(f'Ошибка в handle_gameboard_callback: {e}', exc_info=True)
        bot.send_message(call.from_user.id, 'Произошла ошибка при выполнении команды. Попробуй позже')


def get_current_symbol(game_id: int, current_turn_id: int) -> str:
    """Возвращает символ текущего игрока."""
    player1_id = GAMES_DICT[game_id]['player1']['id']
    return GAMES_DICT[game_id]['player1']['symbol'] if current_turn_id == player1_id else GAMES_DICT[game_id]['player2']['symbol']


def bot_move(game_id: int) -> tuple[int, int]:
    """Делает ход бота, используя алгоритм минимакс, и возвращает координаты хода."""
    board = GAMES_DICT[game_id]['board']
    bot_symbol = GAMES_DICT[game_id]['player2']['symbol']
    player1_symbol = GAMES_DICT[game_id]['player1']['symbol']
    
    def win_combinations():
        return [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]              
        ]

    def check_winner(symbol):
        for combo in win_combinations():
            if all(board[i // 3][i % 3].text == symbol for i in combo):
                return True
        return False

    def empty_squares():
        return [i for i in range(9) if board[i // 3][i % 3].text == "⬜"]

    def make_move(move, symbol):
        board[move // 3][move % 3].text = symbol

    def undo_move(move):
        board[move // 3][move % 3].text = "⬜"

    def minimax(position, maximizing_player):
        if check_winner(bot_symbol):
            return 10
        elif check_winner(player1_symbol):
            return -10
        elif not empty_squares():
            return 0

        if maximizing_player:
            max_eval = -float('inf')
            for move in empty_squares():
                make_move(move, bot_symbol)
                eval = minimax(position, False)
                undo_move(move)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in empty_squares():
                make_move(move, player1_symbol)
                eval = minimax(position, True)
                undo_move(move)
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move():
        best_val = -float('inf')
        best_move = None
        
        for move in empty_squares():
            make_move(move, bot_symbol)
            move_val = minimax(board, False)
            undo_move(move)
            
            if move_val > best_val:
                best_val = move_val
                best_move = move
                
        return best_move

    best_move = find_best_move()
    if best_move is not None:
        return best_move // 3, best_move % 3

    return None, None