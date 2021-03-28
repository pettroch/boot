from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Клавитура Меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('🔺 Инвестиции'), KeyboardButton('🤝 Партнерам')
        ],

        [
            KeyboardButton('💳 Кошелёк'), KeyboardButton('🏆 Информация')
        ],
    ],

    resize_keyboard=True
)


info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('🙏🏼 Хочу такого же бота'), KeyboardButton('💸 Выплаты с бота')
        ],

        [
            KeyboardButton('❤️ Отзывы'), KeyboardButton('💬 Чат')
        ],
    ],

    resize_keyboard=True
)
