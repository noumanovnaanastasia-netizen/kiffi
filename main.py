import os
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from telebot import TeleBot, types

# Пытаемся импортировать базу данных. Если файла еще нет, бот не упадет.
try:
    import database
    HAS_DATABASE = True
except ImportError:
    HAS_DATABASE = False

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)


# =====================================================================
#  ⚙️ ТВОИ НАСТРОЙКИ (ВСТАВЬ СВОИ ССЫЛКИ ВНУТРИ КАВЫЧЕК 👇)
# =====================================================================

# 1. Твой ГЛАВНЫЙ баннер (показывается при команде /start)
URL_MAIN_IMG = "https://t.me/banerss777/9"

# 2. Твои ссылки на статьи и посты
URL_INSTRUCTION_POST = "https://t.me/kiffissT/2"
URL_AGREE = "https://t.me/kiffissT/2"

# 3. ЮЗ твоего бота поддержки (ОБЯЗАТЕЛЬНО с @ в начале!)
HELP_BOT_USERNAME = "@helpkifis_bot"

# =====================================================================

clean_username = HELP_BOT_USERNAME.replace("@", "").strip()
URL_HELP_BOT = f"https://t.me/helpkifis_bot"


# --- ТВОЯ ОБНОВЛЕННАЯ БАЗА ПРОМОКОДОВ ---
PROMO_DATABASE = {
    # Коды на бесплатные дни (выдают готовые ключи сразу)
    "FERgJaff6": {"type": "key", "value": "ss://Y2hvbWVkYWhhaGFoYUBteS12cG4tdGVzdC1rZXk6MTIzNDU=#KiffisTunnel-2Days-Combo"},
    "Ksndbifk":  {"type": "key", "value": "ss://ZnJlZXZwbmZvcmV2ZXJAbXktdnBuLXRlc3Qta2V5OjU0MzIx#KiffisTunnel-1Day-Proxy"},
    "Kanekfmuygw":{"type": "key", "value": "ss://YW5kcm9pZHZwbmJrZXlobmZzZGJpZmtoYmZzZGJmOjU1NTU=#KiffisTunnel-3Days-Proxy"},
    "Hosgimaa":  {"type": "key", "value": "vless://white-list-3days-test-key-location-v2ray-ng#KiffisTunnel-3Days-WL"},
    "ZiXasss":   {"type": "key", "value": "vless://white-list-1day-test-key-location-v2ray-ng#KiffisTunnel-1Day-WL"},

    # Коды на баланс (НАСТОЯЩЕЕ зачисление Звёзд в Supabase!)
    "K1ffissqop": {"type": "stars", "amount": 5},
    "Vuuslnh":     {"type": "stars", "amount": 10},
    "hiskhfie":   {"type": "stars", "amount": 15},
    "Hshsifoq":   {"type": "stars", "amount": 20},
    "GooFfsirn":  {"type": "stars", "amount": 30},

    # Купоны на скидки (выдают красивый текст для поддержки)
    "otKraatoo":   {"type": "text", "value": f"🎫 **Купон на скидку -10% к 1-й покупке!**\n\nПерешли это сообщение в поддержку {HELP_BOT_USERNAME}."},
    "Kiffiss_neabow":{"type": "text", "value": f"🎫 **Купон на скидку -30% к любой покупке!**\n\nПерешли это сообщение в поддержку {HELP_BOT_USERNAME}."},
    "Goalsshould": {"type": "text", "value": f"🎫 **Купон на скидку -10 Звёзд (при покупке от 30 Stars)!**\n\nПерешли это сообщение в поддержку {HELP_BOT_USERNAME}."},
    "EREgoEr3":    {"type": "text", "value": f"🎫 **Купон на скидку -20 Звёзд (при покупке от 45 Stars)!**\n\nПерешли это сообщение в поддержку {HELP_BOT_USERNAME}."}
}


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
    balance = 0
    
    # Безопасная работа с базой данных через подушку безопасности
    if HAS_DATABASE:
        try:
            # Пытаемся зарегистрировать пользователя в таблице Kiffi
            database.register_user(message.from_user.id, message.from_user.username)
            
            # Пытаемся получить его актуальные данные
            user_info = database.get_user_data(message.from_user.id)
            
            # Безопасно вытаскиваем баланс из первой строчки ответа базы данных
            if user_info and isinstance(user_info, list) and len(user_info) > 0:
                balance = user_info[0].get("balance", 0)
        except Exception as e:
            logging.error(f"Скрытая ошибка базы данных: {e}")
            balance = 0 # Если база упала, просто показываем баланс 0 и не ломаем бота

    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("🌐 Просто VPN", callback_data="menu_vpn"), types.InlineKeyboardButton("🧦 Прокси", callback_data="menu_proxy"))
    markup.row(types.InlineKeyboardButton("🤍 Белые списки", callback_data="menu_wl"), types.InlineKeyboardButton("🔄 VPN + БС (Комбо)", callback_data="menu_combo"))
    markup.row(types.InlineKeyboardButton("📖 Инструкция", url=URL_INSTRUCTION_POST), types.InlineKeyboardButton("🎟 Промокоды", callback_data="menu_promo"))
    markup.row(types.InlineKeyboardButton("🆘 Помощь", url=URL_HELP_BOT), types.InlineKeyboardButton("📄 Соглашение", url=URL_AGREE))
    
    bot.send_photo(
        message.chat.id,
        photo=URL_MAIN_IMG,
        caption=f"🔮 **Привет, {message.from_user.first_name}!**\n\n"
                f"💰 Твой баланс: **{balance} ⭐️ Telegram Stars**\n\n"
                f"Добро пожаловать в туннель *Kiffis Tunnel*.\nВыбери необходимую услугу в меню ниже 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )


# --- ОБРАБОТКА НАЖАТИЙ НА КНОПКИ (CALLBACKS) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "menu_promo":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        
        sent_msg = bot.send_message(
            call.message.chat.id, 
            "🎟 **Активация промокода**\n\nВведите секретный промокод в ответном сообщении 👇"
        )
        bot.register_next_step_handler(sent_msg, process_promo_code)
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, text="Эта функция в разработке 🛠")


# --- ЛОГИКА ПРОВЕРКИ ПРОМОКОДА ---
def process_promo_code(message):
    user_text = message.text.strip()
    user_id = message.from_user.id
    
    if user_text in PROMO_DATABASE:
        promo_data = PROMO_DATABASE[user_text]
        
        if promo_data["type"] == "key":
            success_text = f"🎉 **Промокод успешно активирован!**\n\n🎁 Держи твой тестовый ключ:\n\n`{promo_data['value']}`"
            bot.send_message(message.chat.id, success_text, parse_mode="Markdown")
            
        elif promo_data["type"] == "stars":
            amount = promo_data["amount"]
            
            # Безопасное начисление звезд в базу данных
            if HAS_DATABASE:
                try:
                    database.add_stars_to_balance(user_id, amount)
                except Exception as e:
                    logging.error(f"Не удалось начислить звезды в БД: {e}")
            
            success_text = f"🎉 **Успешно!**\n\nНа твой баланс начислено **+{amount} ⭐️ Telegram Stars**!"
            bot.send_message(message.chat.id, success_text, parse_mode="Markdown")
            
        elif promo_data["type"] == "text":
            bot.send_message(message.chat.id, f"🎉 **Промокод распознан!**\n\n{promo_data['value']}", parse_mode="Markdown")
    else:
        bot.send_message(
            message.chat.id, 
            "❌ **Такого промокода не существует!**\n\nПопробуйте снова через меню `/start`.",
            parse_mode="Markdown"
        )


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
