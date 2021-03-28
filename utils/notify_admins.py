import logging

from aiogram import Dispatcher

from data.config import admins
from utils.db_api.db import Db


# Уведомление админу о запуске бота
async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот успешно запущен")

        except Exception as err:
            logging.exception(err)

    # Создание базы данных при запуске
    db = Db()
    db.create()
