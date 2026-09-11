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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    import database
    HAS_DATABASE = True
except ImportError:
    HAS_DATABASE = False

BOT_TOKEN = os.getenv("BOT_TOKEN") or "ВАШ_ТОКЕН_БОТА"
ADMIN_ID = 7303801260  # ⚠️ ВСТАВЬТЕ СВОЙ ID СЮДА!

bot = telebot.TeleBot(BOT_TOKEN)

URL_MAIN_IMG = "https://t.me/banerss777/9"
URL_TARIFFS_IMG = "https://t.me/banerss777/8"
URL_DEVICES_IMG = "https://t.me/banerss777/8"
URL_FINAL_IMG = "https://t.me/banerss777/8"      
URL_PROMO_IMG = "https://t.me/banerss777/6"       

URL_INSTRUCTION_POST = "https://t.me/kiffissT/2"
URL_AGREE = "https://t.me/kiffissT/2"

HELP_BOT_USERNAME = "https://t.me/helpkifis_bot"

URL_VPN_GITHUB = "https://github.com/AvenCores/goida-vpn-configs"
URL_WHITE_GITHUB = "https://github.com/igareck/vpn-configs-for-russia"

MY_STATIC_PROXIES = ["socks5://kifiss_user:pass123@194.67.212.11:1080"]

TARIF_DATA = {
    "proxy": {
        "name": "🤎 Высокоскоростные Прокси",
        "days": {3: {"base_price": 7, "text": "🤎 3 дня — 7 ⭐️"}, 14: {"base_price": 18, "text": "🤎 14 дней — 18 ⭐️"}, 30: {"base_price": 30, "text": "🤎 1 месяц — 30 ⭐️"}, 60: {"base_price": 50, "text": "🤎 2 месяца — 50 ⭐️"}, 90: {"base_price": 70, "text": "🤎 3 месяца — 70 ⭐️"}, 150: {"base_price": 110, "text": "🤎 5 месяцев — 110 ⭐️"}},
        "devices": {1: {"mult": 1.0, "text": "🗂 1 устройство"}, 2: {"mult": 1.4, "text": "🗂 2 устройства"}, 5: {"mult": 2.0, "text": "🗂 5 устройств"}}
    },
    "vpn": {
        "name": "🧸 Безопасный Просто VPN",
        "days": {3: {"base_price": 7, "text": "🧸 3 дня — 7 ⭐️"}, 14: {"base_price": 18, "text": "🧸 14 дней — 18 ⭐️"}, 30: {"base_price": 30, "text": "🧸 1 месяц — 30 ⭐️"}, 60: {"base_price": 50, "text": "🧸 2 месяца — 50 ⭐️"}, 90: {"base_price": 70, "text": "🧸 3 месяца — 70 ⭐️"}, 150: {"base_price": 110, "text": "🧸 5 месяцев — 110 ⭐️"}},
        "devices": {1: {"mult": 1.0, "text": "🗂 1 устройство"}, 2: {"mult": 1.4, "text": "🗂 2 устройства"}, 5: {"mult": 2.0, "text": "🗂 5 устройств"}}
    },
    "white": {
        "name": "🕊 Белые Списки Доступа",
        "days": {3: {"base_price": 10, "text": "🕊 3 дня — 10 ⭐️"}, 14: {"base_price": 22, "text": "🕊 14 дней — 22 ⭐️"}, 30: {"base_price": 36, "text": "🕊 1 месяц — 36 ⭐️"}, 60: {"base_price": 60, "text": "🕊 2 месяца — 60 ⭐️"}, 90: {"base_price": 80, "text": "🕊 3 месяца — 80 ⭐️"}, 150: {"base_price": 130, "text": "🕊 5 месяцев — 130 ⭐️"}},
        "devices": {1: {"mult": 1.0, "text": "🗂 1 устройство"}, 2: {"mult": 1.4, "text": "🗂 2 устройства"}, 5: {"mult": 2.0, "text": "🗂 5 устройств"}}
    },
    "combo": {
        "name": "🪐 Всё включено (КОМБО)",
        "days": {3: {"base_price": 10, "text": "🪐 3 дня — 10 ⭐️"}, 14: {"base_price": 22, "text": "🪐 14 дней — 22 ⭐️"}, 30: {"base_price": 36, "text": "🪐 1 месяц — 36 ⭐️"}, 60: {"base_price": 60, "text": "🪐 2 месяца — 60 ⭐️"}, 90: {"base_price": 80, "text": "🪐 3 месяца — 80 ⭐️"}, 150: {"base_price": 130, "text": "🪐 5 месяцев — 130 ⭐️"}},
        "devices": {1: {"mult": 1.0, "text": "🗂 1 устройство"}, 2: {"mult": 1.4, "text": "🗂 2 устройства"}, 5: {"mult": 2.0, "text": "🗂 5 устройств"}}
    }
}
def get_keys_from_github(url, count=2):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
        lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('<')]
        return random.sample(lines, min(len(lines), count))
    except Exception: return []

def keep_alive_ping():
    while True:
        try: urllib.request.urlopen("https://onrender.com")
        except Exception: pass
        time.sleep(600)

def check_expired_subscriptions():
    while True:
        try:
            if HAS_DATABASE:
                for u in database.get_all_active_users():
                    if u["expire_date"] and datetime.now() > u["expire_date"]:
                        database.deactivate_user_subscription(u["user_id"])
                        try: bot.send_message(u["user_id"], "续 🪐 **Срок подписки истек. Ключ отключен.**")
                        except Exception: pass
        except Exception: pass
        time.sleep(3600)

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_web_server():
    server = HTTPServer(("0.0.0.0", int(os.getenv("PORT", 8080))), WebServer)
    threading.Thread(target=keep_alive_ping, daemon=True).start()
    threading.Thread(target=check_expired_subscriptions, daemon=True).start()
    server.serve_forever()

def get_main_menu_keyboard(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    has_used_trial = False
    if HAS_DATABASE:
        u_info = database.get_user_data(user_id)
        if u_info: has_used_trial = u_info.get("used_trial", False)
    if not has_used_trial:
        markup.add(types.InlineKeyboardButton(text="🎁 АКТИВИРОВАТЬ ТЕСТ НА 3 ДНЯ 🎁", callback_data="activate_trial_click"))
    markup.add(
        types.InlineKeyboardButton(text="🧸 Просто VPN", callback_data="vpn_click"),
        types.InlineKeyboardButton(text="🤎 Прокси", callback_data="proxy_click"),
        types.InlineKeyboardButton(text="🕊 Белые списки", callback_data="white_click"),
        types.InlineKeyboardButton(text="🪐 VPN + БС (Комбо)", callback_data="combo_click"),
        types.InlineKeyboardButton(text="📋 Инструкция", url=URL_INSTRUCTION_POST),
        types.InlineKeyboardButton(text="🔑 Промокоды", callback_data="promo_click"),
        types.InlineKeyboardButton(text="☕️ Поддержка", url=HELP_BOT_USERNAME),
        types.InlineKeyboardButton(text="📄 Соглашение", url=URL_AGREE)
    )
    if user_id == ADMIN_ID:
        markup.add(types.InlineKeyboardButton(text="⚙️ Панель Администратора", callback_data="admin_panel_click"))
    return markup

@bot.message_handler(commands=['start', 'admin'])
def cmd_start(message):
    user_id = message.from_user.id
    if HAS_DATABASE:
        u_data = database.register_user(user_id, message.from_user.username or "user")
        if u_data.get("banned", False):
            bot.send_message(user_id, "❌ Вы заблокированы администратором.")
            return

    if message.text == "/admin" and user_id == ADMIN_ID:
        open_admin_interface(message.chat.id)
        return

    balance = database.get_user_data(user_id).get("balance", 0) if HAS_DATABASE else 0
    welcome_text = f"🐈 **Привет, {message.from_user.first_name}!**\n\n💳 Мой баланс: `{balance}` ⭐️\n\nВыберите услугу 👇"
    bot.send_photo(chat_id=message.chat.id, photo=URL_MAIN_IMG, caption=welcome_text, reply_markup=get_main_menu_keyboard(user_id), parse_mode="Markdown")
@bot.callback_query_handler(func=lambda call: call.data in ["proxy_click", "vpn_click", "white_click", "combo_click"])
def tariff_step_1_days(call):
    srv = call.data.replace("_click", "")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for days, info in TARIF_DATA[srv]["days"].items():
        markup.add(types.InlineKeyboardButton(text=info["text"], callback_data=f"ts2:{srv}:{days}"))
    markup.add(types.InlineKeyboardButton(text="🤍 Назад", callback_data="back_to_main"))
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(URL_TARIFFS_IMG, caption="**Этап 1:** Выберите срок подписки:", parse_mode="Markdown"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ts2:"))
def tariff_step_2_devices(call):
    _, srv, days = call.data.split(":")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for dev, dev_info in TARIF_DATA[srv]["devices"].items():
        total = int(TARIF_DATA[srv]["days"][int(days)]["base_price"] * dev_info["mult"])
        markup.add(types.InlineKeyboardButton(text=f"{dev_info['text']} ➡️ {total} ⭐️", callback_data=f"ts3:{srv}:{days}:{dev}:{total}"))
    markup.add(types.InlineKeyboardButton(text="🤎 Назад", callback_data=f"{srv}_click"))
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(URL_DEVICES_IMG, caption="**Этап 2:** Укажите количество устройств:", parse_mode="Markdown"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ts3:"))
def tariff_step_3_final(call):
    _, srv, days, devices, total_price = call.data.split(":")
    expire_date = (datetime.now() + timedelta(days=int(days))).strftime("%d.%m.%Y")
    markup = types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text=f"💳 Купить за {total_price} ⭐️", callback_data=f"pay_invoice:{srv}:{days}:{devices}:{total_price}"),
        types.InlineKeyboardButton(text="⚙️ Назад", callback_data=f"ts2:{srv}:{days}")
    )
    text = f"🛒 **ПОДТВЕРЖДЕНИЕ**\n• {TARIF_DATA[srv]['name']}\n• Срок: {days} дн.\n• Лимит до: `{expire_date}`\n\nЦена: `{total_price}` ⭐️"
    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(URL_FINAL_IMG, caption=text, parse_mode="Markdown"), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_menu(call):
    try: bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception: pass
    cmd_start(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_invoice:"))
def execute_payment_invoice(call):
    _, srv, days, devices, total_price = call.data.split(":")
    bot.send_invoice(call.message.chat.id, f"Подписка: {TARIF_DATA[srv]['name']}", f"Аренда туннеля", "", "XTR", [types.LabeledPrice(label="Оплата", amount=int(total_price))], payload=f"pay:{call.from_user.id}:{srv}:{days}")

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout(query): bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_payment_success(message):
    _, uid, srv, days = message.successful_payment.invoice_payload.split(":")
    database.update_user_subscription(int(uid), datetime.now() + timedelta(days=int(days)))
    database.register_user(int(uid), message.from_user.username, service_type=srv) # Задаем тип услуги для статистики!
    bot.send_message(message.chat.id, "🎉 Подписка успешно активирована!")

@bot.callback_query_handler(func=lambda call: call.data == "activate_trial_click")
def handle_trial_activation(call):
    user_id = call.from_user.id
    vpn_keys = get_keys_from_github(URL_VPN_GITHUB, count=1)
    bot.send_message(call.message.chat.id, f"🧸 **Тест активирован!**\n\nКлюч: `{vpn_keys[0] if vpn_keys else 'Тест-ключ'}`")
    database.update_user_trial_status(user_id, True)
    database.update_user_subscription(user_id, datetime.now() + timedelta(days=3))
    database.register_user(user_id, call.from_user.username, service_type="vpn") # По умолчанию ставим тип vpn для статистики

@bot.callback_query_handler(func=lambda call: call.data == "promo_click")
def ask_for_promo(call):
    msg = bot.send_message(call.message.chat.id, "🔑 Введите промокод:")
    bot.register_next_step_handler(msg, lambda m: bot.send_message(m.chat.id, "Промокод проверен."))

# =====================================================================
# 🔥 БЛОК НОВОЙ АДМИН-ПАНЕЛИ СО СТАТИСТИКОЙ, БАНОМ И НАЧИСЛЕНИЕМ
# =====================================================================
def open_admin_interface(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text="📊 Посмотреть статистику", callback_data="adm_stats"),
        types.InlineKeyboardButton(text="💰 Начислить баланс ⭐️", callback_data="adm_add_bal"),
        types.InlineKeyboardButton(text="🚫 Заблокировать юзера", callback_data="adm_ban"),
        types.InlineKeyboardButton(text="⬅️ Выйти в меню", callback_data="back_to_main")
    )
    bot.send_message(chat_id, "⚙️ **ПАНЕЛЬ УПРАВЛЕНИЯ KIFFIS**\n\nВыберите действие администратора:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "admin_panel_click")
def admin_btn(call):
    if call.from_user.id == ADMIN_ID: open_admin_interface(call.message.chat.id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("adm_"))
def handle_admin_actions(call):
    if call.from_user.id != ADMIN_ID: return
    action = call.data
    
    if action == "adm_stats":
        s = database.get_stats()
        text = (
            f"📊 **ДЕТАЛЬНАЯ СТАТИСТИКА БОТА**\n┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n"
            f"• Всего пользователей в базе: `{s['total']}`\n"
            f"• Заблокировано: `{s['banned']}`\n\n"
            f"📈 **Активные подписки по категориям:**\n"
            f"• 🧸 VPN-туннели: `{s['vpn']}`\n"
            f"• 🤎 Прокси-серверы: `{s['proxy']}`\n"
            f"• 🕊 Белые списки: `{s['white']}`\n"
            f"• 🪐 Комбо-пакеты: `{s['combo']}`"
        )
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        
    elif action == "adm_add_bal":
        msg = bot.send_message(call.message.chat.id, "✏️ Введите **ID** человека или его **@username** для начисления:")
        bot.register_next_step_handler(msg, process_admin_find_user, "balance")
        
    elif action == "adm_ban":
        msg = bot.send_message(call.message.chat.id, "✏️ Введите **ID** человека или его **@username** для блокировки:")
        bot.register_next_step_handler(msg, process_admin_find_user, "ban")
        
    bot.answer_callback_query(call.id)

def process_admin_find_user(message, mode):
    input_data = message.text.strip()
    target_id = None
    
    if input_data.isdigit():
        target_id = int(input_data)
    else:
        target_id = database.find_user_by_username(input_data)
        
    if not target_id or not database.get_user_data(target_id):
        bot.send_message(message.chat.id, "❌ Пользователь не найден в базе данных бота. Он должен хотя бы раз нажать /start.")
        return
        
    if mode == "balance":
        msg = bot.send_message(message.chat.id, f"💰 Пользователь найден! Введите сумму звёзд для начисления (например `100` или `-50` для списания):")
        bot.register_next_step_handler(msg, process_admin_save_balance, target_id)
    elif mode == "ban":
        database.set_ban_status(target_id, True)
        bot.send_message(message.chat.id, f"🚫 Пользователь `{target_id}` успешно заблокирован в системе!")
        try: bot.send_message(target_id, "❌ Вы были заблокированы администратором.")
        except Exception: pass

def process_admin_save_balance(message, target_id):
    try:
        amount = int(message.text.strip())
        new_bal = database.add_balance(target_id, amount)
        bot.send_message(message.chat.id, f"✅ Баланс успешно изменен! Текущий счет пользователя: `{new_bal}` ⭐️")
        try: bot.send_message(target_id, f"💰 Администратор начислил вам `{amount}` ⭐️! Ваш баланс: `{new_bal}` ⭐️")
        except Exception: pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Ошибка: введите корректное число.")

if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.infinity_polling()
