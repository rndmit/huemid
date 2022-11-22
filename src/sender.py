from telegram.ext import Updater
from telegram import Bot
import config

class Sender():
    def __init__(self) -> None:
        self.bot = Bot(token=config.TG_BOT_TOKEN)

    def send_result(self, to: str):
        self.bot.send_message(chat_id=to, text="Hi")