from aiogram.types import Message

from loader import dp
from keyboards.default.reply_keyboard import menu


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='❤️ Отзывы', state='*')
async def buttonReviews(message: Message):
    await message.answer('''Здесь Вы можете почитать отзывы о боте: @Company_otzyv''', reply_markup=menu)