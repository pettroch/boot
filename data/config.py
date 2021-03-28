import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN")) # Получение токена бота
QIWI_PRIVATE_KEY = str(os.getenv("QIWI_PRIVATE_KEY")) # Получение приватного ключа QIWI
PAY_COMMENT = str(os.getenv("COMMENT_FOR_PAY")) # Получение комментария к платежу

# Получение ид админов из файла .env
admins = [
    os.getenv("ADMIN_ID"),
]

# Получение ip из файла .env
ip = os.getenv("ip")
