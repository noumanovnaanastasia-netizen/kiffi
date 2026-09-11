import logging

# Структура: { user_id: { "username": str, "used_trial": bool, "expire_date": datetime, "balance": int, "banned": bool, "service_type": str } }
_USERS_DB = {}

def register_user(user_id, username, service_type=None):
    """Регистрирует нового пользователя или обновляет его активность"""
    if user_id not in _USERS_DB:
        _USERS_DB[user_id] = {
            "username": str(username).lower().replace("@", ""),
            "used_trial": False,
            "expire_date": None,
            "balance": 0,
            "banned": False,
            "service_type": service_type
        }
        logging.info(f"DB: Зарегистрирован {user_id}")
    elif service_type:
        _USERS_DB[user_id]["service_type"] = service_type
    return _USERS_DB[user_id]

def get_user_data(user_id):
    return _USERS_DB.get(user_id, None)

def find_user_by_username(username):
    """Ищет ID пользователя по его юзернейму"""
    target = str(username).lower().replace("@", "").strip()
    for uid, data in _USERS_DB.items():
        if data.get("username") == target:
            return uid
    return None

def add_balance(user_id, amount):
    """Начисляет или списывает (если чило отрицательное) баланс звёзд"""
    if user_id in _USERS_DB:
        _USERS_DB[user_id]["balance"] += amount
        return _USERS_DB[user_id]["balance"]
    return None

def set_ban_status(user_id, is_banned=True):
    """Блокирует или разблокирует пользователя"""
    if user_id in _USERS_DB:
        _USERS_DB[user_id]["banned"] = is_banned
        return True
    return False

def get_stats():
    """Собирает подробную статистику по пользователям и типам услуг"""
    total = len(_USERS_DB)
    banned = sum(1 for u in _USERS_DB.values() if u.get("banned", False))
    vpn_users = sum(1 for u in _USERS_DB.values() if u.get("service_type") == "vpn")
    proxy_users = sum(1 for u in _USERS_DB.values() if u.get("service_type") == "proxy")
    white_users = sum(1 for u in _USERS_DB.values() if u.get("service_type") == "white")
    combo_users = sum(1 for u in _USERS_DB.values() if u.get("service_type") == "combo")
    
    return {
        "total": total, "banned": banned,
        "vpn": vpn_users, "proxy": proxy_users,
        "white": white_users, "combo": combo_users
    }

def update_user_trial_status(user_id, used_trial=True):
    if user_id in _USERS_DB: _USERS_DB[user_id]["used_trial"] = used_trial

def update_user_subscription(user_id, expire_date):
    if user_id in _USERS_DB: _USERS_DB[user_id]["expire_date"] = expire_date

def get_all_active_users():
    return [{"user_id": uid, "expire_date": d["expire_date"]} for uid, d in _USERS_DB.items() if d.get("expire_date")]

def deactivate_user_subscription(user_id):
    if user_id in _USERS_DB: _USERS_DB[user_id]["expire_date"] = None
