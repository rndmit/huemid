#!/usr/bin/env python3
import time
import os
import pathlib
from ksuid import ksuid
from telegram import Bot
from src.scrapper import Scrapper
import config

if __name__ == '__main__':
    chat_id = config.TG_CHAT_ID
    run_id = ksuid().__str__()
    bot = Bot(token=config.TG_BOT_TOKEN)
    scr = Scrapper()

    bot.send_message(chat_id,
                     text=f'Run {run_id} started at {time.asctime()}')
    scr.run(run_id)
    result_img = open(pathlib.PurePath(os.getcwd(), 'results', run_id).with_suffix('.png'), 'rb')
    bot.send_photo(chat_id, photo=result_img)
