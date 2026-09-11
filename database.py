import logging

# Простая база данных в оперативной памяти 
# Хранит информацию в формате: { user_id: { "used_trial": True/False, "expire_date": datetime, "balance": 0 } }
_USERS_DB = {}

def register_user(user_id, username):
    """Регистрирует нового пользователя, если его нет в базе, и ВСЕГДА возвращает его данные"""
    if user_id not in _USERS_DB:
        _USERS_DB[user_id] = {
            "username": username,
            "used_trial": False,
            "expire_date": None,
            "balance": 0
        }
        logging.info(f"DB: Пользователь {user_id} (@{username}) успешно зарегистрирован.")
    
    # Исправлено: теперь данные возвращаются всегда, даже при повторном старте
    return _USERS_DB[user_id]

def get_user_data(user_id):
    """Возвращает данные пользователя по его ID. Если пользователя нет, возвращает пустой словарь во избежание NoneType ошибок"""
    return _USERS_DB.get(user_id, {
        "username": "Пользователь",
        "used_trial": False,
        "expire_date": None,
        "balance": 0
    })

def update_user_trial_status(user_id, used_trial=True):
    """Обновляет статус использования бесплатного триала"""
    if user_id in _USERS_DB:
        _USERS_DB[user_id]["used_trial"] = used_trial
        return True
    return False

def update_user_subscription(user_id, expire_date):
    """Обновляет дату окончания платной подписки пользователя"""
    if user_id in _USERS_DB:
        _USERS_DB[user_id]["expire_date"] = expire_date
        return True
    return False

def get_all_active_users():
    """Возвращает список всех пользователей, у которых установлена дата окончания подписки"""
    active_users = []
    for uid, data in _USERS_DB.items():
        if data.get("expire_date") is not None:
            active_users.append({
                "user_id": uid,
                "expire_date": data["expire_date"]
            })
    return active_users

def deactivate_user_subscription(user_id):
    """Сбрасывает подписку пользователя при истечении срока"""
    if user_id in _USERS_DB:
        _USERS_DB[user_id]["expire_date"] = None
        return True
    return False
