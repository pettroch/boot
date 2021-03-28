import os

from aiogram.types import Message

from loader import dp, bot
from keyboards.default.reply_keyboard import menu
from keyboards.inline.inline_keyboard import wallet
from utils.db_api.db import Db


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='💳 Кошелёк', state='*')
async def buttonWallet(message: Message):
    pathToImg = os.path.normpath(os.getcwd() + os.sep + '\\img\\wallet.png')
    img = open(pathToImg, 'rb')

    db = Db()
    data = db.getOneRecord(message.from_user.id)

    balance_personal = data[1]
    balance_for_invest = data[4]

    await bot.send_photo(message.chat.id, img, caption=f'''<b>Ваш ID:</b> {message.from_user.id}
💰 <b>Ваш личный баланс</b>: {balance_personal}₽
💰 <b>Баланс для инвестиций:</b> {balance_for_invest}₽
''', reply_markup=wallet)