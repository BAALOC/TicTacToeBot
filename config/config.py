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
GAMES_DICT = {}