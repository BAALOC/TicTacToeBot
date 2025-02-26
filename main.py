from utils import logger

import handlers  # noqa
from database import create_models
from loader import bot
from utils import set_default_commands


if __name__ == '__main__':
    logger.info('Запуск программы')
    
    create_models()
    logger.info('Создание моделей')

    set_default_commands(bot)
    logger.info('Установка команд')

    logger.info('Запуск бота')
    bot.infinity_polling()
