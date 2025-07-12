from datetime import datetime, timedelta,timezone
from app.models.types.user import UserSession,User
from app.models.types.auth import OauthToken
from app.core.redis_client import redis_client
from app.core.exceptions import AuthenticationError
from app.core.config import settings
import httpx 
from fastapi import HTTPException
# TODO: Writing a singleton decorator instance of of decorated class
# To maintain unified db connection of redis to store tokens 


async def save_tokens(token,user_id: str):
    if 'expires_in' in token:
    # If token has expires_in, convert to expires_at
        expires_at = int(datetime.now(timezone.utc).timestamp()) + token['expires_in']
        token['expires_at'] = expires_at
        token.pop('expires_in', None)  

    user_oauth_token = OauthToken(**token) 
    await redis_client.set(f"user:{user_id}:token",user_oauth_token.model_dump_json())

async def save_session(session_data: dict, session_token: str):
    session = UserSession(**session_data)  # Pydantic validation
    await redis_client.set(f"session:{session_token}:session",session.model_dump_json())

async def save_user(user_id: str, user_data: dict):
    user = User(**user_data)  # Pydantic validation
    await redis_client.set(f"user:{user_id}:data", user.model_dump_json())

async def get_access_token(user_id: str):
    token_raw_data = redis_client.get(f"user:{user_id}:token")
    if not token_raw_data:
        return None
    return User.model_validate_json(token_raw_data) #type: ignore

async def get_valid_access_token(user_id: str):
    token_data = await redis_client.get(f"user:{user_id}:token")
    if not token_data:
        return None
    token = OauthToken.model_validate_json(token_data)  # type: ignore                                    
    if token.expires_at - int(datetime.now(timezone.utc).timestamp()) < 3600:  # type: ignore
        return await get_refresh_token(user_id)
    return token  # type: ignore

async def get_refresh_token(user_id: str):
    token_data = await redis_client.get(f"user:{user_id}:token")
    if not token_data:
        raise AuthenticationError("No token found for user")
    token = OauthToken.model_validate_json(token_data)  # type: ignore
    refresh_token =  token.refresh_token 
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token

    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")
    
    token_data = response.json
    await save_tokens(token_data,user_id="shrish")

    return token_data
    