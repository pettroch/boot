import logging

from aiogram.types import Message

from loader import dp
from data.config import admins
from keyboards.default.reply_keyboard import menu
from utils.stateMachine import StateMachine


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='!sponsor', state='*')
async def sponsor(message: Message):
    for admin in admins:
        try:
            if message.from_user.id == int(admin):
                try:
                    await dp.bot.send_message(message.from_user.id, 'Введите спонсора:')
                    state = dp.current_state(user=message.from_user.id)
                    await state.set_state(StateMachine.all()[5])
                except:
                    pass

        except Exception as err:
            logging.exception(err)
