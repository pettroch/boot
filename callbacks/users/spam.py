from aiogram.types import CallbackQuery, Message

from loader import dp, bot
from utils.db_api.db import Db
from data.config import admins
from utils.stateMachine import StateMachine


@dp.message_handler(state=StateMachine.STATE_4)
async def getAmountFromUser(message: Message):
    text = message.text

    db = Db()

    users = []
    allUsers = db.getAllUsers()

    for items in allUsers:
        users.append(items[0])

    print(users)

    for user in users:
        try:
            await bot.send_message(user, text)
        except:
            print('Error spam')

    for admin in admins:
        try:
            await bot.send_message(admin, 'Текст отправлен')
        except:
            pass

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(StateMachine.all()[0])
        