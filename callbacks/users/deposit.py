from aiogram.types import CallbackQuery, Message

from loader import dp, bot
from utils.db_api.db import Db
from utils.qiwi_api import qiwi
from utils.stateMachine import StateMachine
from keyboards.inline.inline_keyboard import check_status_pay


# Депозит
@dp.callback_query_handler(lambda c: c.data == 'deposit', state='*')
async def process_callback_buttonDeposit(callback_query: CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(StateMachine.all()[1])

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'''💰 <b>Мин. сумма депозита:</b> <i>1 ₽.</i>

📥 Пополнение Вашего баланса проводится через платежную систему <i>"QIWI"</i>.

💬 <b><i>Введите в чат сумму пополнения:</i></b>''')

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.message_handler(state=StateMachine.STATE_1)
async def getAmountFromUser(message: Message):
    amount = message.text
    db = Db()

    try:
        if amount.isdigit():
            amount = int(amount)

            if amount >= 1:
                invoice = qiwi.create_invoice(amount)
                pay_url = invoice.pay_url
                bill_id = invoice.bill_id
                
                db.updateBillId(bill_id, message.from_user.id)
                db.updateWaitingAmount(amount, message.from_user.id)

                await bot.send_message(message.from_user.id, f'🚀 Ссылка для оплаты счета: \n\n{pay_url}')

                await bot.send_message(message.from_user.id, '⚠️ Нажмите кнопку ниже, чтобы проверить статус платежа',
                    reply_markup=check_status_pay)

            elif amount < 1:
                db.updateBillId(0, message.from_user.id)
                await bot.send_message(message.from_user.id, '''❗️ <b>Мин. сумма пополнения равна 1 руб.</b>''')
        
        else:
            db.updateBillId(0, message.from_user.id)
            await bot.send_message(message.from_user.id, '''❗️ <b>Ошибка: неверный формат</b>''')

        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StateMachine.all()[0])
    
    except:
        pass
        