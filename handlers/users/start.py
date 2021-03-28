from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api.db import Db
from keyboards.default.reply_keyboard import menu


# Вывод сообщения Пользователю, когда он запустил бота или ввел команду /start
@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    db = Db()
    db.addSponsor('')
    sponsor = db.getSponsor()[0][0]

    await dp.bot.send_message(message.from_user.id, f' ✅Что бы начать зарабатывать нужно обязательно оформить подписку на: {sponsor}')

    if len(message.text) > 6:
        bossId = int(message.text[7:]) # из ссылки
        
        referalId = message.from_user.id

        data = db.getOneRecord(bossId)

        db.addNewUser(message.from_user.id) # Добавление нового Пользователя в базу данных
        referalIsExists = db.addReferal(bossId, referalId)
        
        countReferals = data[7]
        your_vklad = data[2]
        referals = db.getReferals(bossId)

        for item in referals:
            if bossId == item[0] and referalId == item[1]:
                try:
                    if referalIsExists:
                        await dp.bot.send_message(bossId, f'''🏆 Вы получили <b>7 руб.</b> за реферала @{message.from_user.username}''')
                        db.updateCountReferals(bossId, countReferals + 1)
                        db.updateYourVklad(bossId, your_vklad + 7)
                
                except:
                    pass

        await message.answer(f'''Выберите действие ⤵️''',
            reply_markup=menu
        )       

    else:
        db = Db()
        db.addNewUser(message.from_user.id)

        await message.answer(f'''Выберите действие ⤵️''',
            reply_markup=menu
        )
