from aiogram.types import Message

from loader import dp
from keyboards.default.reply_keyboard import menu


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='💬 Чат', state='*')
async def buttonChat(message: Message):
    await message.answer(f'''Ссылка на чат: https://t.me/joinchat/QohoU_7SbwMwYjZi''', reply_markup=menu)