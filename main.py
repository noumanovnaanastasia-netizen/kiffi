import os
import logging
import threading
import time
import random
import urllib.request
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot
from telebot import types

# 1. НАСТРОЙКА ЛОГИРОВАНИЯ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. ПОДКЛЮЧЕНИЕ БАЗЫ ДАННЫХ
try:
    import database
    HAS_DATABASE = True
    logging.info("Система: Локальная база данных успешно подключена.")
except ImportError:
    HAS_DATABASE = False
    logging.warning("Система: Файл database.py не найден. Бот работает без сохранения триалов!")

# 3. ИНИЦИАЛИЗАЦИЯ БОТА
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = "ВАШ_ТОКЕН_БОТА" 

bot = telebot.TeleBot(BOT_TOKEN)

# 4. ДАННЫЕ О ССЫЛКАХ И БАННЕРАХ
URL_MAIN_IMG = "https://t.me/banerss777/9"        # Главный котик
URL_TARIFFS_IMG = "https://t.me/banerss777/8"     # Баннер выбора дней (Шаг 1)
URL_DEVICES_IMG = "https://t.me/banerss777/8"     # Баннер выбора устройств (Шаг 2)
URL_FINAL_IMG = "https://t.me/banerss777/8"       # Финальный чек оплаты (Шаг 3)
URL_PROMO_IMG = "https://t.me/banerss777/6"       # Раздел промокодов и триала

URL_INSTRUCTION_POST = "https://t.me/kiffissT/2"
URL_AGREE = "https://t.me/kiffissT/2"
HELP_BOT_USERNAME = "https://t.me/helpkifis_bot"

# Репозитории на GitHub с вашими ключами (Замените на свои RAW ссылки)
URL_VPN_GITHUB = "https://github.com/AvenCores/goida-vpn-configs"
URL_WHITE_GITHUB = "https://github.com/igareck/vpn-configs-for-russia"

# Статический список ваших личных прокси-серверов
MY_STATIC_PROXIES = [
    "socks5://user:pass@192.168.1.1:1080",
    "socks5://user:pass@192.168.1.2:1080"
]

# 5. СЕТКА ТАРИФОВ И СТОИМОСТЬ В TELEGRAM STARS ⭐️
TARIF_DATA = {
    "proxy": {
        "name": "🚀 Скоростные Прокси",
        "days": {
            3: {"base_price": 7, "text": "🗓 3 дня — 7 ⭐️"},
            14: {"base_price": 18, "text": "🗓 14 дней — 18 ⭐️"},
            30: {"base_price": 30, "text": "🗓 1 месяц — 30 ⭐️"},
            60: {"base_price": 50, "text": "🗓 2 месяца — 50 ⭐️"},
            90: {"base_price": 70, "text": "🗓 3 месяца — 70 ⭐️"},
            150: {"base_price": 110, "text": "🗓 5 месяцев — 110 ⭐️"}
        },
        "devices": {
            1: {"mult": 1.0, "text": "📱 1 устройство"},
            2: {"mult": 1.4, "text": "📱 2 устройства (Скидка!)"},
            5: {"mult": 2.0, "text": "📱 5 устройств (Мега-скидка!)"}
        }
    },
    "vpn": {
        "name": "🌐 Защищенный Просто VPN",
        "days": {
            3: {"base_price": 7, "text": "🗓 3 дня — 7 ⭐️"},
            14: {"base_price": 18, "text": "🗓 14 дней — 18 ⭐️"},
            30: {"base_price": 30, "text": "🗓 1 месяц — 30 ⭐️"},
            60: {"base_price": 50, "text": "🗓 2 месяца — 50 ⭐️"},
            90: {"base_price": 70, "text": "🗓 3 месяца — 70 ⭐️"},
            150: {"base_price": 110, "text": "🗓 5 месяцев — 110 ⭐️"}
        },
        "devices": {
            1: {"mult": 1.0, "text": "📱 1 устройство"},
            2: {"mult": 1.4, "text": "📱 2 устройства (Скидка!)"},
            5: {"mult": 2.0, "text": "📱 5 устройств (Мега-скидка!)"}
        }
    },
    "white": {
        "name": "⚪️ Приоритетные Белые Списки",
        "days": {
            3: {"base_price": 10, "text": "🗓 3 дня — 10 ⭐️"},
            14: {"base_price": 22, "text": "🗓 14 дней — 22 ⭐️"},
            30: {"base_price": 36, "text": "🗓 1 месяц — 36 ⭐️"},
            60: {"base_price": 60, "text": "🗓 2 месяца — 60 ⭐️"},
            90: {"base_price": 80, "text": "🗓 3 месяца — 80 ⭐️"},
            150: {"base_price": 130, "text": "🗓 5 месяцев — 130 ⭐️"}
        },
        "devices": {
            1: {"mult": 1.0, "text": "📱 1 устройство"},
            2: {"mult": 1.4, "text": "📱 2 устройства (Скидка!)"},
            5: {"mult": 2.0, "text": "📱 5 устройств (Мега-скидка!)"}
        }
    },
    "combo": {
        "name": "🔥 Всё включено (КОМБО-Тариф)",
        "days": {
            3: {"base_price": 10, "text": "🗓 3 дня — 10 ⭐️"},
            14: {"base_price": 22, "text": "🗓 14 дней — 22 ⭐️"},
            30: {"base_price": 36, "text": "🗓 1 месяц — 36 ⭐️"},
            60: {"base_price": 60, "text": "🗓 2 месяца — 60 ⭐️"},
            90: {"base_price": 80, "text": "🗓 3 месяца — 80 ⭐️"},
            150: {"base_price": 130, "text": "🗓 5 месяцев — 130 ⭐️"}
        },
        "devices": {
            1: {"mult": 1.0, "text": "📱 1 устройство"},
            2: {"mult": 1.4, "text": "📱 2 устройства (Скидка!)"},
            5: {"mult": 2.0, "text": "📱 5 устройств (Мега-скидка!)"}
        }
    }
}
# =====================================================================
# 6. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И ФОНОВЫЕ ПОТОКИ (ПИНГ И КРОН)
# =====================================================================
def get_keys_from_github(url, count=2):
    """Скачивает текстовый файл с GitHub и выбирает случайные строки"""
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode('utf-8')
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        return random.sample(lines, min(len(lines), count))
    except Exception as e:
        logging.error(f"Ошибка чтения GitHub: {e}")
        return []

def keep_alive_ping():
    """Фоновый поток само-пинга, защищающий Render от засыпания"""
    RENDER_URL = "https://onrender.com" 
    while True:
        try:
            urllib.request.urlopen(RENDER_URL)
            logging.info("Пинг-Воркер: Успешный пинг. Сервер бодрствует!")
        except Exception as e:
            logging.error(f"Пинг-Воркер: Ошибка пинга: {e}")
        time.sleep(600)

def check_expired_subscriptions():
    """Фоновый проверяльщик истекших подписок (срабатывает раз в час)"""
    while True:
        try:
            if HAS_DATABASE:
                active_users = database.get_all_active_users()
                now = datetime.now()
                for user in active_users:
                    uid = user["user_id"]
                    expire_date = user["expire_date"]
                    if expire_date and now > expire_date:
                        database.deactivate_user_subscription(uid)
                        try:
                            bot.send_message(
                                uid,
                                "🚨 **Срок действия вашей подписки истек.**\n\n"
                                "Ваш туннель автоматически деактивирован. "
                                "Вы можете мгновенно продлить её в главном меню бота! ⭐️",
                                parse_mode="Markdown"
                            )
                        except Exception:
                            pass
        except Exception as e:
            logging.error(f"Крон-Воркер: Ошибка проверки лимитов: {e}")
        time.sleep(3600)

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Kiffis Tunnel работает!".encode("utf-8"))

def run_web_server():
    from http.server import HTTPServer
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), WebServer)
    logging.info(f"Сервер: Веб-интерфейс развернут на порту {port}")
    threading.Thread(target=keep_alive_ping, daemon=True).start()
    threading.Thread(target=check_expired_subscriptions, daemon=True).start()
    server.serve_forever()

# =====================================================================
# 7. ЛОГИКА ИНТЕРФЕЙСА ТЕЛЕГРАМ (КНОПКИ И ОБРАБОТЧИКИ)
# =====================================================================
def get_main_menu_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    help_url = f"https://t.me{HELP_BOT_USERNAME.replace('@','')}" if not HELP_BOT_USERNAME.startswith('http') else HELP_BOT_USERNAME
    markup.add(
        types.InlineKeyboardButton(text="🌐 Просто VPN", callback_data="vpn_click"),
        types.InlineKeyboardButton(text="🦫 Прокси", callback_data="proxy_click"),
        types.InlineKeyboardButton(text="🤍 Белые списки", callback_data="white_click"),
        types.InlineKeyboardButton(text="🌌 VPN + БС (Комбо)", callback_data="combo_click"),
        types.InlineKeyboardButton(text="📖 Инструкция ↗️", url=URL_INSTRUCTION_POST),
        types.InlineKeyboardButton(text="🎁 Промокоды", callback_data="promo_click"),
        types.InlineKeyboardButton(text="🆘 Помощь ↗️", url=help_url),
        types.InlineKeyboardButton(text="📄 Соглашение ↗️", url=URL_AGREE)
    )
    return markup

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Пользователь"
    balance = 0
    if HAS_DATABASE:
        user_data = database.register_user(user_id, username)
        balance = user_data.get("balance", 0)

    welcome_text = (
        f"🔮 **Привет, {message.from_user.first_name}!**\n\n"
        f"💰 Твой баланс: {balance} ⭐️ Telegram Stars\n\n"
        f"Добро пожаловать в туннель **Kiffis Tunnel**.\n"
        f"Выбери необходимую услугу в меню ниже 👇"
    )
    bot.send_photo(chat_id=message.chat.id, photo=URL_MAIN_IMG, caption=welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")
# --- ПОШАГОВЫЙ КАЛЬКУЛЯТОР ТАРИФОВ С УЧЁТОМ МЕДИА-БАННЕРОВ ---

@bot.callback_query_handler(func=lambda call: call.data in ["proxy_click", "vpn_click", "white_click", "combo_click"])
def tariff_step_1_days(call):
    service_map = {"proxy_click": "proxy", "vpn_click": "vpn", "white_click": "white", "combo_click": "combo"}
    srv = service_map[call.data]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for days, info in TARIF_DATA[srv]["days"].items():
        markup.add(types.InlineKeyboardButton(text=info["text"], callback_data=f"ts2:{srv}:{days}"))
    markup.add(types.InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_main"))
    
    text = f"💳 **{TARIF_DATA[srv]['name']}**\n\n**Шаг 1 из 2:** Выберите необходимый срок действия подписки из тарифной сетки:"
    
    # Плавное переключение на баннер тарифов
    try:
        bot.edit_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            media=types.InputMediaPhoto(URL_TARIFFS_IMG, caption=text, parse_mode="Markdown"),
            reply_markup=markup
        )
    except Exception:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ts2:"))
def tariff_step_2_devices(call):
    _, srv, days = call.data.split(":")
    days = int(days)
    markup = types.InlineKeyboardMarkup(row_width=1)
    base_price = TARIF_DATA[srv]["days"][days]["base_price"]
    
    for dev, dev_info in TARIF_DATA[srv]["devices"].items():
        current_total = int(base_price * dev_info["mult"])
        markup.add(types.InlineKeyboardButton(text=f"{dev_info['text']} ➡️ {current_total} ⭐️", callback_data=f"ts3:{srv}:{days}:{dev}:{current_total}"))
        
    markup.add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{srv}_click"))
    text = f"💳 **{TARIF_DATA[srv]['name']}**\n📋 Срок подписки: {days} дней\n\n**Шаг 2 из 2:** Укажите количество подключаемых устройств:"
    
    # Плавное переключение на баннер выбора устройств
    try:
        bot.edit_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            media=types.InputMediaPhoto(URL_DEVICES_IMG, caption=text, parse_mode="Markdown"),
            reply_markup=markup
        )
    except Exception:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ts3:"))
def tariff_step_3_final(call):
    _, srv, days, devices, total_price = call.data.split(":")
    days = int(days)
    expire_date = (datetime.now() + timedelta(days=days)).strftime("%d.%m.%Y")
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text=f"🚀 ОПЛАТИТЬ ПАКЕТ ЗА {total_price} ⭐️", callback_data=f"pay_invoice:{srv}:{days}:{devices}:{total_price}"),
        types.InlineKeyboardButton(text="⚙️ Изменить параметры", callback_data=f"ts2:{srv}:{days}")
    )
    
    text = (
        f"🛒 **ПОДТВЕРЖДЕНИЕ ЗАКАЗА**\n\n"
        f"• **Услуга:** {TARIF_DATA[srv]['name']}\n"
        f"• **Период:** {days} дней\n"
        f"• **Устройства:** {devices} шт.\n"
        f"• **Активен до:** `{expire_date}` 📅\n\n"
        f"💵 **Итого к оплате:** `{total_price}` Telegram Stars ⭐️"
    )
    
    # Плавное переключение на баннер финального чека
    try:
        bot.edit_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            media=types.InputMediaPhoto(URL_FINAL_IMG, caption=text, parse_mode="Markdown"),
            reply_markup=markup
        )
    except Exception:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_menu(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    cmd_start(call.message)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "promo_click")
def handle_trial_and_promos(call):
    user_id = call.from_user.id
    has_used_trial = False
    if HAS_DATABASE:
        user_info = database.get_user_data(user_id)
        if user_info:
            has_used_trial = user_info.get("used_trial", False)
            
    if has_used_trial:
        bot.send_message(call.message.chat.id, "❌ **Пробный период завершен**\n\nВы уже использовали свои бесплатные 3 дня. Продлите подписку в меню! ⭐️")
        bot.answer_callback_query(call.id)
        return

    # Загружаем промо-баннер на место котика
    text_loading = "⏳ Генерируем тестовые ключи на 3 дня..."
    try:
        bot.edit_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            media=types.InputMediaPhoto(URL_PROMO_IMG, caption=text_loading, parse_mode="Markdown"),
            reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main"))
        )
    except Exception:
        pass

    vpn_keys = get_keys_from_github(URL_VPN_GITHUB, count=2)
    white_keys = get_keys_from_github(URL_WHITE_GITHUB, count=3)
    proxy_key = random.choice(MY_STATIC_PROXIES) if MY_STATIC_PROXIES else "Нет свободных прокси"

    output_text = (
        "🎁 **Ваш бесплатный пробный период (3 дня) АКТИВИРОВАН!**\n\n"
        f"🍏 **Прокси:** `{proxy_key}`\n\n"
        "🌐 **VPN (2 шт.):**\n"
    )
    for i, k in enumerate(vpn_keys, 1):
        output_text += f"{i}. `{k}`\n"
    output_text += "\n⚪️ **Белые списки:**\n"
    for i, k in enumerate(white_keys, 1):
        output_text += f"{i}. `{k}`\n"

    bot.send_message(call.message.chat.id, output_text, parse_mode="Markdown")
    if HAS_DATABASE:
        database.update_user_trial_status(user_id, used_trial=True)
        database.update_user_subscription(user_id, datetime.now() + timedelta(days=3))
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_invoice:"))
def execute_payment_invoice(call):
    bot.send_message(call.message.chat.id, "🏗 Шлюз Stars-инвойсов подготовлен к работе.")
    bot.answer_callback_query(call.id)

if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    logging.info("Система: Telegram-бот успешно запущен!")
    bot.infinity_polling()
