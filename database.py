import os
import requests
import logging

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Настройка заголовков для авторизации в Supabase
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def register_user(user_id: int, username: str):
    """Проверяет пользователя в базе Kiffi. Если его нет — регистрирует."""
    url = f"{SUPABASE_URL}/rest/v1/Kiffi?user_id=eq.{user_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200 and not response.json():
            # Пользователя нет в БД -> создаем запись
            insert_url = f"{SUPABASE_URL}/rest/v1/Kiffi"
            data = {
                "user_id": user_id,
                "username": username or "Unknown",
                "balance": 0,
                "vpn_until": None
            }
            requests.post(insert_url, headers=HEADERS, json=data)
            logging.info(f"Пользователь {user_id} успешно добавлен в базу Kiffi!")
    except Exception as e:
        logging.error(f"Ошибка при регистрации в Supabase: {e}")

def get_user_data(user_id: int):
    """Получает все данные пользователя из базы Kiffi."""
    url = f"{SUPABASE_URL}/rest/v1/Kiffi?user_id=eq.{user_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200 and response.json():
            return response.json()[0] # Возвращаем первую строку с данными
    except Exception as e:
        logging.error(f"Ошибка получения данных из Supabase: {e}")
    return None

def add_stars_to_balance(user_id: int, stars_amount: int):
    """Начисляет Звёзды на баланс пользователя в базе Kiffi."""
    user_data = get_user_data(user_id)
    if not user_data:
        return False
    
    current_balance = user_data.get("balance", 0)
    new_balance = current_balance + stars_amount
    
    url = f"{SUPABASE_URL}/rest/v1/Kiffi?user_id=eq.{user_id}"
    data = {"balance": new_balance}
    try:
        res = requests.patch(url, headers=HEADERS, json=data)
        return res.status_code in [200, 201, 204]
    except Exception as e:
        logging.error(f"Ошибка обновления баланса: {e}")
        return False
