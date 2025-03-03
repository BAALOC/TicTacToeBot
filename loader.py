from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config import BOT_TOKEN

storage = StateMemoryStorage()
bot = TeleBot(token=BOT_TOKEN, state_storage=storage)
