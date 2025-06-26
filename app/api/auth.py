import httpx
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
import urllib.parse
from app.core.config import settings
from app.api.token_store import (
    save_tokens,
    get_access_token,
    get_refresh_token,
    save_session,
    save_user
)
from app.models.types.auth import CodePayload, RefreshPayload, TokenResponse

router = APIRouter()

# In production, use a database (redis) to store user session
# TODO:
# change the order of calls when cookies are implemented
# to get user_id from cookies and if tokens present then refresh, create session, save tokens
# and return session token
@router.post("/code")
async def exchange_code(payload: CodePayload):
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": payload.code,
        "redirect_uri": settings.DISCORD_REDIRECT_URI,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # change the order of calls when cookies are implemented
    # to get user_id from cookies and then save the tokens
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.DISCORD_API_BASE_URL}/oauth2/token", data=data, headers=headers)

    if response.status_code != 200:
        print("Discord token exchange failed:", response.status_code, response.text)
        raise HTTPException(status_code=400, detail="Token exchange failed")
    token_data = response.json()

    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://discord.com/api/users/@me",
            headers={
                "Authorization": f"Bearer {token_data['access_token']}"
            }
        )
    if user_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user data")
    
    user_data = user_response.json()
    session_token = str(uuid.uuid4())
    

    save_tokens(token_data, user_id=user_data["id"])
    save_user(user_data,user_data["id"])
    save_session(user_data, session_token)

    return user_data

@router.post("/refresh")
async def refresh_token(user_id: str):
    refresh_token = get_refresh_token(user_id)
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
    save_tokens(token_data,user_id="shrish")

    return token_data
# SECTION: Bot Authentication Features
# TODO: Add bot authentication
#       Support additional parameters and handle scenarios beyond standard bot scope.
@router.post("/bot")
async def bot_authentication(guild_id: str):
    """
    Authenticate a bot for a specific guild.
    This endpoint is for bot-specific authentication and may require additional parameters.
    """
    scope = "bot+applications.commands"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "scope": scope,
        "permissions": 364870364415, 
        "guild_id": guild_id,
        "disable_guild_select": "true",

    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.DISCORD_API_BASE_URL}/oauth2/authorize", headers=headers, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Bot authentication failed")

    token_data = response.json()
    save_tokens(token_data, user_id="bot")

    return token_data

# Reference: https://discord.com/developers/docs/topics/oauth2#revoking-a-token

# SECTION: OAuth2 Enhancements
# TODO: Implement token revocation
#       Revoke user tokens securely using Discord's OAuth2 revoke endpoint.
# TODO: Add refresh fallback logic
#       Automatically refresh tokens on expiry and retry failed API calls.






