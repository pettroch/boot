from aiogram.types import Message

from loader import dp
from keyboards.default.reply_keyboard import menu


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(commands=['menu'], state='*')
async def showMenu(message: Message):
    await message.answer('Клавиатура показана 🎹', reply_markup=menu)