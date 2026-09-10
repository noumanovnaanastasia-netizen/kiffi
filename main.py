import os
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from telebot import TeleBot, types

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)


# =====================================================================
#  ⚙️ ТВОИ ССЫЛКИ ДЛЯ НАСТРОЙКИ (МЕНЯЙ ССЫЛКИ ВНУТРИ КАВЫЧЕК 👇)
# =====================================================================

# 1. Твой ГЛАВНЫЙ баннер (который показывается при команде /start)
URL_MAIN_IMG = "https://t.me/banerss777/9"

# 2. Твои ссылки на статьи и посты
URL_INSTRUCTION_POST = "https://t.me/kiffissT/2"
URL_AGREE = "https://t.me/kiffissT/2"

# 3. Ссылка на твоего ОТДЕЛЬНОГО бота поддержки (замени юзернейм на своего)
URL_HELP_BOT = "https://t.me/helpkifis_bot"

# =====================================================================


# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Kiffis Tunnel работает!".encode("utf-8"))

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), WebServer)
    logging.info(f"Веб-сервер запущен на порту {port}")
    server.serve_forever()


# --- ГЛАВНОЕ МЕНЮ ---
@bot.message_handler(commands=['start'])
def cmd_start(message):
    markup = types.InlineKeyboardMarkup()
    
    # 1 ряд: VPN и Прокси
    btn_vpn = types.InlineKeyboardButton("🌐 Просто VPN", callback_data="menu_vpn")
    btn_proxy = types.InlineKeyboardButton("🧦 Прокси", callback_data="menu_proxy")
    markup.row(btn_vpn, btn_proxy)
    
    # 2 ряд: Белые списки и Комбо
    btn_wl = types.InlineKeyboardButton("🤍 Белые списки", callback_data="menu_wl")
    btn_combo = types.InlineKeyboardButton("🔄 VPN + БС (Комбо)", callback_data="menu_combo")
    markup.row(btn_wl, btn_combo)
    
    # 3 ряд: Инструкция и Промокоды
    btn_ins = types.InlineKeyboardButton("📖 Инструкция", url=URL_INSTRUCTION_POST) 
    btn_promo = types.InlineKeyboardButton("🎟 Промокоды", callback_data="menu_promo")
    markup.row(btn_ins, btn_promo)
    
    # 4 ряд: Помощь (теперь ведет прямо в бота поддержки) и Соглашение
    btn_help = types.InlineKeyboardButton("🆘 Помощь", url=URL_HELP_BOT)
    btn_agree = types.InlineKeyboardButton("📄 Соглашение", url=URL_AGREE)
    markup.row(btn_help, btn_agree)
    
    bot.send_photo(
        message.chat.id,
        photo=URL_MAIN_IMG,
        caption=f"🔮 **Привет, {message.from_user.first_name}!**\n\nДобро пожаловать в туннель *Kiffis Tunnel*.\nВыбери необходимую услугу в меню ниже 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )


# --- ОБРАБОТКА НАЖАТИЙ (ДЛЯ ОСТАЛЬНЫХ КНОПОК) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    bot.answer_callback_query(call.id, text="Эта функция в разработке 🛠")


if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    logging.info("Сброс старых сессий Telegram...")
    try:
        bot.remove_webhook()
    except Exception as e:
        logging.warning(f"Не удалось удалить вебхук: {e}")
        
    time.sleep(2)
    
    logging.info("Бот Kiffis Tunnel успешно запущен...")
    bot.infinity_polling(skip_pending=True)
