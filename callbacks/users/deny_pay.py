from aiogram.types import CallbackQuery, Message

import logging

from data.config import admins
from loader import dp, bot
from utils.db_api.db import Db
from utils.qiwi_api import qiwi
from utils.stateMachine import StateMachine
from keyboards.inline.inline_keyboard import check_status_pay


# Депозит
@dp.callback_query_handler(lambda c: c.data == 'deny', state='*')
async def process_callback_buttonDenyPay(callback_query: CallbackQuery):
    #state = dp.current_state(user=callback_query.from_user.id)
    #await state.set_state(StateMachine.all()[0])

    await bot.answer_callback_query(callback_query.id)

    db = Db()
    data = db.getOneRecord(callback_query.from_user.id)

    waiting_number = str(data[11])
    waiting_amount = data[10]


    db.updateWaitingNumber(callback_query.from_user.id, 0)
    db.updateWaitingAmount(0, callback_query.from_user.id)

    for admin in admins:
        try:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=f'''💸 Новая заявка на вывод

<b>ID:</b> <i>{callback_query.from_user.id}</i>
<b>Username:</b> <i>@{callback_query.from_user.username}</i>
<b>Кошелек:</b> <i>{waiting_number}</i>
<b>Сумма:</b> <i>{waiting_amount}</i>''' , reply_markup=None)

            await dp.bot.send_message(admin, f'''Вы отклонили заявку''')
        except Exception as err:
            logging.exception(err)