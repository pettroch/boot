from aiogram.types import CallbackQuery, Message

import logging

from data.config import admins
from loader import dp, bot
from utils.db_api.db import Db
from utils.qiwi_api import qiwi
from utils.stateMachine import StateMachine
from keyboards.inline.inline_keyboard import check_status_pay, approve_pay


# Депозит
@dp.callback_query_handler(lambda c: c.data == 'withdraw', state='*')
async def process_callback_buttonWithdraw(callback_query: CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(StateMachine.all()[2])

    try:
        await bot.answer_callback_query(callback_query.id)
    except:
        pass

    await bot.send_message(callback_query.from_user.id, f'''💵 <b>Минимальная сумма вывода на "QIWI" - 1 ₽</b>
<i>* Вывод на "QIWI" моментальный</i>

Введите номер кошелька "QIWI" в чат:
''')

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.message_handler(state=StateMachine.STATE_2)
async def getNumberFromUser(message: Message):
    db = Db()
    number = message.text

    try:
        if number.isdigit():
            db.updateWaitingNumber(message.from_user.id, number)

            await bot.send_message(message.from_user.id, f'''💬 <b>Введите в чат сумму для вывода:</b>''')

            state = dp.current_state(user=message.from_user.id)
            await state.set_state(StateMachine.all()[3])
    except:
        pass


@dp.message_handler(state=StateMachine.STATE_3)
async def getAmountFromUser(message: Message):
    amount = message.text
    db = Db()
    print(1)
    data = db.getOneRecord(message.from_user.id)
    waiting_number = str(data[10])
    balance = data[1]

    try:
        if amount.isdigit():
            amount = int(amount)

            if amount <= balance:
                db.updateWaitingAmount(amount, message.from_user.id)
                #qiwi.send_pay(amount, waiting_number)
                await bot.send_message(message.from_user.id, '''<b>🏧 Ваша заяка отправлена на рассмотрение</b>
                
🚨 Ожидайте, когда Администратор ее рассмотрит.''', reply_markup=None)

                for admin in admins:
                    try:
                        await dp.bot.send_message(admin, f'''💸 Новая заявка на вывод

<b>ID:</b> <i>{message.from_user.id}</i>
<b>Username:</b> <i>@{message.from_user.username}</i>
<b>Кошелек:</b> <i>{waiting_number}</i>
<b>Сумма:</b> <i>{amount}</i>''', reply_markup=approve_pay)

                    except Exception as err:
                        logging.exception(err)

            elif amount < 1:
                db.updateBillId(0, message.from_user.id)
                await bot.send_message(message.from_user.id, '''❗️ <b>Мин. сумма вывода равна 1 руб.</b>''')
        
        else:
            db.updateBillId(0, message.from_user.id)
            await bot.send_message(message.from_user.id, '''❗️ <b>Ошибка: неверный формат</b>''')

        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StateMachine.all()[0])
    
    except:
        pass
