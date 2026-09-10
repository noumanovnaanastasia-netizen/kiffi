import os
import logging
from telebot import TeleBot, types

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

# Ссылка на твой главный баннер (пока тестовая, можешь заменить на свою из telegra.ph)
URL_MAIN_IMG = "https://placehold.co"

@bot.message_handler(commands=['start'])
def cmd_start(message):
    # Создаем клавиатуру
    markup = types.InlineKeyboardMarkup()
    
    # 1 ряд: Просто VPN и Прокси
    btn_vpn = types.InlineKeyboardButton("🌐 Просто VPN", callback_data="menu_vpn")
    btn_proxy = types.InlineKeyboardButton("🧦 Прокси", callback_data="menu_proxy")
    markup.row(btn_vpn, btn_proxy)
    
    # 2 ряд: Белые списки и Комбо
    btn_wl = types.InlineKeyboardButton("🤍 Белые списки", callback_data="menu_wl")
    btn_combo = types.InlineKeyboardButton("🔄 VPN + БС (Комбо)", callback_data="menu_combo")
    markup.row(btn_wl, btn_combo)
    
    # 3 ряд: Инструкция и Промокоды
    # Вместо пустой кнопки сразу встраиваем ссылку на инструкцию, это очень удобно!
    btn_ins = types.InlineKeyboardButton("📖 Инструкция", url="https://telegra.ph") 
    btn_promo = types.InlineKeyboardButton("🎟 Промокоды", callback_data="menu_promo")
    markup.row(btn_ins, btn_promo)
    
    # 4 ряд: Помощь и Соглашение
    btn_help = types.InlineKeyboardButton("🆘 Помощь", callback_data="menu_help")
    btn_agree = types.InlineKeyboardButton("📄 Соглашение", url="https://telegra.ph")
    markup.row(btn_help, btn_agree)
    
    # Отправляем баннер вместе с текстом и кнопками
    bot.send_photo(
        message.chat.id,
        photo=URL_MAIN_IMG,
        caption=f"🔮 **Привет, {message.from_user.first_name}!**\n\nДобро пожаловать в туннель *Kiffis Tunnel*.\nВыбери необходимую услугу в меню ниже 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    logging.info("Бот Kiffis Tunnel обновляется...")
    bot.infinity_polling()
