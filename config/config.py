import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_PATH = 'database.db'
COMMANDS_DESCRIPTION = (
    ('start', 'запустить бота'),
    ('help', 'список команд')
)
GAMES_DICT = {
    # Словарь для хранения информации об играх
    # Ключ - уникальный идентификатор игры (game_id)
    # Значение - словарь с информацией о размере поля, игроках и текущем ходе
    # Пример структуры:
    # {
    #     game_id: {
    #         'size': 3,  # Размер игрового поля
    #         'player1': {  # Информация о первом игроке
    #             'id': 123456,  # ID игрока
    #             'username': 'Игрок1',  # Имя пользователя
    #             'symbol': '❌'  # Символ игрока
    #         },
    #         'player2': {  # Информация о втором игроке (или None, если игрока нет)
    #             'id': 654321,
    #             'username': 'Игрок2',
    #             'symbol': '⭕'
    #         },
    #         'board': [],  # Игровое поле
    #         'current_turn': None  # ID текущего игрока
    #     }
    # }
}