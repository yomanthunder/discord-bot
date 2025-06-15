from datetime import datetime, timedelta

# Global in-memory store (dict acts as a singleton)
# TODO: Writing a singleton decorator instance of of decorated class
#       To maintain unified db connection of --> redis or postgreSql to store tokens 
token_store = {}

def save_tokens(token,user_id: str):
    token_store[user_id] = {
        **token, 
        "expires_at": datetime.now() + timedelta(seconds=token["expires_in"])
    }
    print(token_store[user_id])

def get_access_token(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data["access_token"]

def get_refresh_token(user_id: str):
    token_data = token_store.get(user_id)
    return token_data["refresh_token"] if token_data else None

def get_token_data(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data
def delete_token(user_id: str):
    if user_id in token_store:
        del token_store[user_id]
        return True
    return False
def is_token_valid(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return False

    return token_data["expires_at"] > datetime.now()
def get_all_tokens():
    return {user_id: data for user_id, data in token_store.items() if data["expires_at"] > datetime.now()}
def clear_expired_tokens():
    expired_users = [user_id for user_id, data in token_store.items() if data["expires_at"] < datetime.now()]
    for user_id in expired_users:
        del token_store[user_id]
    return expired_users
def clear_all_tokens():
    token_store.clear()
    return True
    return len(token_store)
def get_token(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data
def update_token(user_id: str, new_token: dict):
    if user_id in token_store:
        token_store[user_id].update(new_token)
        token_store[user_id]["expires_at"] = datetime.now() + timedelta(seconds=new_token["expires_in"])
        return True
    return False
def token_exists(user_id: str):
    return user_id in token_store and token_store[user_id]["expires_at"] > datetime.now()
def get_token_expiry(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data["expires_at"]
def get_token_type(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data.get("token_type", "Bearer")  # Default to "Bearer" if not specified
def get_token_scope(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data.get("scope", "identify")  # Default to "identify" if not specified