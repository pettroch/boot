from aiogram.types import CallbackQuery

from loader import dp, bot
from utils.db_api.db import Db
from utils.qiwi_api import qiwi
from data.config import admins
from keyboards.inline.inline_keyboard import check_status_pay


@dp.callback_query_handler(lambda c: c.data == 'checkstatuspay', state='*')
async def process_callback_buttonCheckStatusPay(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    db = Db()

    data = db.getOneRecord(callback_query.from_user.id)

    bill_id = data[8]
    status = qiwi.checkStatusPay(bill_id)
    waiting_amount = data[9]
    your_vklad = data[2]

    if status == 'WAITING':
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, '🕗 Счет выставлен, ожидает оплаты', reply_markup=check_status_pay)
    
    elif status == 'PAID':
        db.updateYourVklad(callback_query.from_user.id, waiting_amount + your_vklad)
        db.updateBalanceForInvest(callback_query.from_user.id, your_vklad + waiting_amount)
        db.updateWaitingAmount(0, callback_query.from_user.id)
        db.updateBillId(0, callback_query.from_user.id)

        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        
        await bot.send_message(callback_query.message.chat.id, f'✅ <b>Счет оплачен</b>\n\n<b>🏧 Сумма пополнения:</b> <i>{waiting_amount}</i>\n<b>💰 Баланс для инвестиций:</b> <i>{your_vklad + waiting_amount}₽</i>', reply_markup=None)
        
        for admin in admins:
            try:
                userName = callback_query.from_user.username
                await dp.bot.send_message(admin, f'''<b>Пополнение счета</b>
                
<b>Пользователь:</b> @{userName}
<b>Сумма</b>: {waiting_amount}₽''')

            except:
                pass
            
    elif status == 'REJECTED':
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, '🚫 Счет отклонен', reply_markup=check_status_pay)
        
        db.updateWaitingAmount(0, callback_query.from_user.id)
        db.updateBillId(0, callback_query.from_user.id)
        qiwi.rejectInvoice(bill_id)
    
    elif status == 'EXPIRED':
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, '❌ Время ожидания истекло. Счет не оплачен', reply_markup=check_status_pay)
        
        db.updateWaitingAmount(0, callback_query.from_user.id)
        db.updateBillId(0, callback_query.from_user.id)