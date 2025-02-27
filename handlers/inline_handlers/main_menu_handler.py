from loader import bot
from telebot import types
from utils import logger
import uuid

@bot.callback_query_handler(func=lambda call: call.data in ['start_game'])
def handle_main_menu(call: types.CallbackQuery) -> None:
    try:
        if call.data == 'start_game':
            logger.info(f'Пользователь {call.from_user.username}: Запрос на начало игры')
            bot.answer_callback_query(call.id,'Запуск игры...')

            game_id = call.from_user.id
            invite_link = f'https://t.me/TicTacToeBaalocBot?start={game_id}'
            message_text = f'🎮 Отлично! Давай начнем игру!\n\nПерешли это сообщение другу, с которым хочешь сыграть:\n\n{invite_link}\n\n' \
                            '👆 Когда твой друг перейдет по этой ссылке, вы сможете начать игру!'
            bot.send_message(call.from_user.id, message_text)

    except Exception as e:
        logger.error(f'Ошибка в handle_main_menu: {e}', exc_info=True)
        bot.answer_callback_query(call.id, 'Произошла ошибка')
