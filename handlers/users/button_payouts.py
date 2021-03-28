from aiogram.types import Message

from loader import dp
from keyboards.default.reply_keyboard import menu


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='💸 Выплаты с бота', state='*')
async def buttonPayouts(message: Message):
    await message.answer('''Здесь Вы можете почитать отзывы о выплатах: @Company_otzyv''', reply_markup=menu)