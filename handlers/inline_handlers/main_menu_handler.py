from telebot import types
from loader import bot
from utils import logger
from keyboards import get_game_choice_keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def handle_main_menu(call: types.CallbackQuery) -> None:
    """Обрабатывает запрос на начало игры из главного меню."""
    try:
        bot.send_message(call.from_user.id, 'Выбери режим игры 👇:', reply_markup=get_game_choice_keyboard())

    except Exception as e:
        logger.error(f'Ошибка в handle_main_menu: {e}', exc_info=True)
        bot.answer_callback_query(call.id, 'Произошла ошибка при выполнении команды. Попробуй позже')


