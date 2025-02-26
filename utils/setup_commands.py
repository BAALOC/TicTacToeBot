import telebot

from config import COMMANDS_DESCRIPTION


def bot_set_commands(bot: telebot.TeleBot) -> None:
    bot.set_my_commands(
        [telebot.types.BotCommand(*i) for i in COMMANDS_DESCRIPTION]
    )