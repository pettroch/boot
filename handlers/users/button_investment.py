import os
import threading
import time
from datetime import datetime

from aiogram.types import Message

from loader import dp, bot
from keyboards.default.reply_keyboard import menu
from utils.db_api.db import Db


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='🔺 Инвестиции', state='*')
async def buttonInvestment(message: Message):
    pathToImg = os.path.normpath(os.getcwd() + os.sep + '\\img\\investment.png')
    img = open(pathToImg, 'rb')

    db = Db()
    data = db.getOneRecord(message.from_user.id)

    your_vklad = data[2]
    you_earned = data[1]

    await bot.send_photo(message.chat.id, img, caption=f'''Открывай инвестиции и получай стабильную прибыль в данном разделе, после собирай доход:

💰 <b>Процент прибыли:</b> 5%
⏱ <b>Время доходности:</b> 24 часа
📆 <b>Срок вклада:</b> Навсегда

💳 <b>Ваш вклад:</b> {your_vklad}₽
💸 <b>Ваш доход в сутки:</b> {your_vklad * 0.05}₽

🏆 <b>Вы заработали:</b> {you_earned}₽

🧭 Прибыль приходит каждые 24 часа.    
''')

    flag = data[11]

    if flag == 0:
        if your_vklad != 0:
            await bot.send_message(message.from_user.id, 'Заработок начался. Через 24 часа возвращайся снова')
            db.updateTimeFlag(message.from_user.id, 1)
            threading.Thread(target=moneyFarm, args=(message, db, your_vklad,)).start()
        else:
            await bot.send_message(message.from_user.id, 'Ваш баланс для начисления 5% равен 0. Невозможно заработать.')


def moneyFarm(message, db, your_vklad):
    while True:
        data = db.getOneRecord(message.from_user.id)
        your_earned = data[1]

        db.updateYouEarned(message.from_user.id, your_earned + (your_vklad * 0.05))
        time.sleep(86400)
