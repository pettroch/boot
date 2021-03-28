from aiogram.types import CallbackQuery, Message

from loader import dp, bot
from utils.db_api.db import Db
from data.config import admins
from utils.stateMachine import StateMachine


@dp.message_handler(state=StateMachine.STATE_5)
async def getAmountFromUser(message: Message):
    text = message.text

    db = Db()

    for admin in admins:
        try:
            db.updateSponsor(text)
            await bot.send_message(admin, 'Спонсор добавлен')
        except:
            pass

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(StateMachine.all()[0])
        