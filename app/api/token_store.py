from datetime import datetime, timedelta
from app.models.types.user import UserSession

# Global in-memory store (dict acts as a singleton)
# TODO: Writing a singleton decorator instance of of decorated class
#       To maintain unified db connection of --> redis or postgreSql to store tokens 
token_store = {}
session_store = {}
user_store = {}
# Function to save tokens in the global store

def save_tokens(token,user_id: str):
    token_store[user_id] = {
        **token, 
        "expires_at": datetime.now() + timedelta(seconds=token["expires_in"])
    }

def save_session(session_data: dict, session_token: str):
        session_store[session_token] = UserSession(
        user_id= session_data["user_id"],
        username= session_data["username"],
        avatar= session_data["avatar"],
        is_authenticated= True,
    )
def save_user(user_id: str, user_data: dict):
    user_store[user_id] = {
        **user_data
    }     

def get_access_token(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data["access_token"]

def get_refresh_token(user_id: str):
    token_data = token_store.get(user_id)
    if not token_data:
        return None

    if token_data["expires_at"] < datetime.now():
        return None  # Token expired
    return token_data["refresh_token"]