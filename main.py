import os
import logging
from telebot import TeleBot, types

# Включаем логи, чтобы всё видеть
logging.basicConfig(level=logging.INFO)

# Получаем токен из настроек Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(
        message.chat.id, 
        "🔮 Привет! Новый Kiffis Tunnel успешно запущен на ультра-лёгком движке!"
    )

if __name__ == "__main__":
    logging.info("Бот Kiffis Tunnel запускается...")
    # Запуск постоянного опроса сервера Telegram
    bot.infinity_polling()
