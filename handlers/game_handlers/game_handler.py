from telebot import types
from loader import bot
from utils import logger
from config import GAMES_DICT
from handlers.game_handlers.game_utils import send_game_message, validate_move, handle_game_result, update_board, check_game_end
import random


@bot.callback_query_handler(func=lambda call: call.data.startswith('game#'))
def handle_gameboard_callback(call: types.CallbackQuery) -> None:
    """Обрабатывает ход игрока на игровом поле."""
    try:
        game_id, x, y = map(int, call.data.split('#')[1:])

        if not validate_move(game_id, x, y, call):
            return

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
        bot.answer_callback_query(call.id, 'Ход сделан')

    except KeyError:
        logger.warning(f'Игрок {call.from_user.username} пытался сделать ход в несуществующей игре: {game_id}')
        bot.answer_callback_query(call.id, 'Игра не найдена')
    except Exception as e:
        logger.error(f'Ошибка в handle_gameboard_callback: {e}', exc_info=True)
        bot.send_message(call.from_user.id, 'Произошла ошибка при выполнении команды. Попробуй позже')


def get_current_symbol(game_id: int, current_turn_id: int) -> str:
    """Возвращает символ текущего игрока."""
    player1_id = GAMES_DICT[game_id]['player1']['id']
    return GAMES_DICT[game_id]['player1']['symbol'] if current_turn_id == player1_id else GAMES_DICT[game_id]['player2']['symbol']

def bot_move(game_id: int) -> tuple[int, int]:
    """Делает ход бота, сначала блокируя игрока, а затем ставя фишку для победы, и возвращает координаты хода."""
    board = GAMES_DICT[game_id]['board']
    size = GAMES_DICT[game_id]['size']
    bot_symbol = GAMES_DICT[game_id]['player2']['symbol']
    player1_symbol = GAMES_DICT[game_id]['player1']['symbol']
    
    # Проверка на возможность блокировки
    for i in range(size):
        if board[i].count('⬜') == 1 and board[i].count(player1_symbol) == size - 1:
            j = board[i].index('⬜')
            logger.info(f'Бот заблокировал игрока, сделав ход в клетку ({i}, {j}) в игре {game_id}.')
            return i, j

    for j in range(size):
        column = [board[i][j].text for i in range(size)]
        if column.count('⬜') == 1 and column.count(player1_symbol) == size - 1:
            i = column.index('⬜')
            logger.info(f'Бот заблокировал игрока, сделав ход в клетку ({i}, {j}) в игре {game_id}.')
            return i, j

    diagonal1 = [board[i][i].text for i in range(size)]
    if diagonal1.count('⬜') == 1 and diagonal1.count(player1_symbol) == size - 1:
        i = diagonal1.index('⬜')
        logger.info(f'Бот заблокировал игрока, сделав ход в клетку ({i}, {i}) в игре {game_id}.')
        return i, i

    diagonal2 = [board[i][size - 1 - i].text for i in range(size)]
    if diagonal2.count('⬜') == 1 and diagonal2.count(player1_symbol) == size - 1:
        i = diagonal2.index('⬜')
        logger.info(f'Бот заблокировал игрока, сделав ход в клетку ({i}, {size - 1 - i}) в игре {game_id}.')
        return i, size - 1 - i
    
    # Проверка на возможность выигрыша
    for i in range(size):
        if board[i].count('⬜') == 1 and board[i].count(bot_symbol) == size - 1:
            j = board[i].index('⬜')
            logger.info(f'Бот выиграл, сделав ход в клетку ({i}, {j}) в игре {game_id}.')
            return i, j

    for j in range(size):
        column = [board[i][j].text for i in range(size)]
        if column.count('⬜') == 1 and column.count(bot_symbol) == size - 1:
            i = column.index('⬜')
            logger.info(f'Бот выиграл, сделав ход в клетку ({i}, {j}) в игре {game_id}.')
            return i, j

    diagonal1 = [board[i][i].text for i in range(size)]
    if diagonal1.count('⬜') == 1 and diagonal1.count(bot_symbol) == size - 1:
        i = diagonal1.index('⬜')
        logger.info(f'Бот выиграл, сделав ход в клетку ({i}, {i}) в игре {game_id}.')
        return i, i

    diagonal2 = [board[i][size - 1 - i].text for i in range(size)]
    if diagonal2.count('⬜') == 1 and diagonal2.count(bot_symbol) == size - 1:
        i = diagonal2.index('⬜')
        logger.info(f'Бот выиграл, сделав ход в клетку ({i}, {size - 1 - i}) в игре {game_id}.')
        return i, size - 1 - i

    # Если нет угрозы, делаем случайный ход
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j].text == '⬜']
    if empty_cells:
        i, j = random.choice(empty_cells)
        logger.info(f'Бот сделал случайный ход в клетку ({i}, {j}) в игре {game_id}.')

        return i, j

    return None, None