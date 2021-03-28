from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


wallet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='➕ Пополнить', callback_data='deposit'),
            InlineKeyboardButton(text='➖ Вывести', callback_data='withdraw')
        ],
    ],

    resize_keyboard=True
)


check_status_pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Проверить 👁', callback_data='checkstatuspay')
        ]
    ]
)

approve_pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Одобрить', callback_data='approve'),
            InlineKeyboardButton(text='Отказать', callback_data='deny')
        ]
    ]
)