from utils import logger
import handlers  # noqa
from database import create_models
from loader import bot
from utils import bot_setup_commands

def main():
    """Основная функция запуска бота."""
    try:
        logger.info('Запуск программы')

        create_models()
        logger.info('Создание моделей')

        bot_setup_commands(bot)
        logger.info('Установка команд')
        
        logger.info('Запуск бота')
        bot.infinity_polling()

    except Exception as e:
        logger.error(f'Ошибка в main.py: {e}', exc_info=True)

if __name__ == '__main__':
    main()
