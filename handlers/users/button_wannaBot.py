from aiogram.types import Message

from loader import dp
from keyboards.default.reply_keyboard import menu


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='🙏🏼 Хочу такого же бота', state='*')
async def buttonWannaBot(message: Message):
    await message.answer('''Свяжись с разработчиком, чтобы получить такого же бота: @weil_joseph''', reply_markup=menu)