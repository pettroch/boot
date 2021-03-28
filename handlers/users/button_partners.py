import os

from aiogram.types import Message
from aiogram.utils.deep_linking import get_start_link

from loader import dp, bot
from keyboards.default.reply_keyboard import menu
from utils.db_api.db import Db


# Вывод сообщения при активации команды /menu. Показывает клавиатуру
@dp.message_handler(text='🤝 Партнерам', state='*')
async def buttonPartners(message: Message):
    pathToImg = os.path.normpath(os.getcwd() + os.sep + '/img/partners.png')
    img = open(pathToImg, 'rb')

    db = Db()
    count_referals = db.getAllCountReferals(message.from_user.id)[0]

    link = await get_start_link(message.from_user.id)

    await bot.send_photo(message.chat.id, img, caption=f'''<b>Наша партнерская программа считается самой эффективной, приглашай друзей и получай за это деньги.</b>
    
💰 <b>За каждого реферала вы будете получать:</b> <i>7₽</i> сразу же на инвестиции и <i>15%</i> от инвестиций реферала на баланс для вывода.

👥 <b>Партнеров:</b> {count_referals} чел.
🔗 <b>Ваша реф-ссылка: </b>{link}
''')
