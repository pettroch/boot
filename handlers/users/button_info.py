import os

from aiogram.types import Message

from loader import dp, bot
from keyboards.default.reply_keyboard import menu, info
from utils.db_api.db import Db


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='🏆 Информация', state='*')
async def buttonInfo(message: Message):
    pathToImg = os.path.normpath(os.getcwd() + os.sep + '\\img\\info.png')
    img = open(pathToImg, 'rb')

    db = Db()
    countInvesters = db.getAllCountInvesters()

    await bot.send_photo(message.chat.id, img, caption=f'''<b>Вы попали в раздел настройки бота, здесь вы можете посмотреть статистику, а также узнать информацию или отключить уведомления.</b>

🌐 <b>Работаем с:</b> 25.03
👥 <b>Всего инвесторов:</b> {countInvesters}
🗣 <b>Новых за 24 часа:</b> {countInvesters}
''', reply_markup=info)