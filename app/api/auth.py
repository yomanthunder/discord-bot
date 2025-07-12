import httpx
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from  urllib.parse import urlencode
from app.core.config import settings
from loguru import logger
from app.services.token_store import (
    save_tokens,
    get_access_token,
    get_refresh_token,
    save_session,
    save_user
)
from app.models.types.auth import CodePayload, RefreshPayload, TokenResponse

router = APIRouter()
class botRequest(BaseModel):
    user_id: str
    guild_id: str
# In production, use a database (redis) to store user session
# TODO:
# change the order of calls when cookies are implemented
# to get user_id from cookies and if tokens present then refresh, create session, save tokens
# and return session token
@router.post("/code")
async def exchange_code(payload:CodePayload):
    if not payload.code:
        raise HTTPException(status_code=400, detail="Autherisation Code is required")
    
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
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
            if response.status_code != 200:
                logger.error(f"Discord token exchange failed: {response.status_code} - {response.text}")
                raise HTTPException(status_code=400, detail="Authentication failed")
            if response.status_code != 200:
                print("Discord token exchange failed:", response.status_code, response.text)
                logger.error(f"Discord token exchange failed: {response.status_code} - {response.text}")
                raise HTTPException(status_code=400, detail="Token exchange failed")
            token_data = response.json()
            print(token_data)
            user_response = await client.get(
                "https://discord.com/api/users/@me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
                timeout=10.0
            )
            
            if user_response.status_code != 200:
                logger.error(f"Failed to fetch Discord user data: {user_response.status_code}")
                raise HTTPException(status_code=400, detail="Failed to fetch user data")
            
            user_data = user_response.json()
            print(user_data)

    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Request timeout")
    except httpx.RequestError as e:
        logger.error(f"Request error during Discord OAuth: {e}")
        raise HTTPException(status_code=500, detail="External service error")
    
    try:
        await save_tokens(token_data, user_id=user_data["id"])
        await save_user(user_id=user_data["id"], user_data=user_data)
        session_token = str(uuid.uuid4())
        session_data = {
            "user_id": user_data["id"],
            "username": user_data["username"],
            "global_name": user_data.get("global_name", None),
            "is_authenticated": True
        }
        await save_session(session_data= session_data ,session_token=session_token)
    except Exception as e:
        logger.error(f"Error saving tokens or user data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return {"session_token": session_token, "user_id": user_data["id"]}

# @router.post("/refresh")
# async def refresh_token(user_id: str):
#     refresh_token = get_refresh_token(user_id)
#     data = {
#         "client_id": settings.DISCORD_CLIENT_ID,
#         "client_secret": settings.DISCORD_CLIENT_SECRET,
#         "grant_type": "refresh_token",
#         "refresh_token": refresh_token

#     }
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
#     if response.status_code != 200:
#         raise HTTPException(status_code=400, detail="Token exchange failed")
    
#     token_data = response.json
#     await save_tokens(token_data,user_id="shrish")

#     return token_data


# SECTION: Bot Authentication Features
# TODO: Add bot authentication
#       Support additional parameters and handle scenarios beyond standard bot scope.
@router.post("/bot")
async def bot_authentication(user_request: botRequest):
    user_id = user_request.user_id
    guild_id = user_request.guild_id
    
    if not user_id or not guild_id:
        raise HTTPException(status_code=400, detail="User ID and Guild ID are required")
    
    # Build the authorization URL for bot installation
    params = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "scope": "bot applications.commands",  # Note: space, not +
        "permissions": "364870364415",
        "guild_id": guild_id,
        "disable_guild_select": "true"
    }
    
    # Generate the URL that the user needs to visit
    auth_url = f"{settings.DISCORD_API_BASE_URL}/oauth2/authorize?" + urlencode(params)
    
    return {
        "authorization_url": auth_url,
        "message": "Please visit this URL to add the bot to your guild"
    }

# Reference: https://discord.com/developers/docs/topics/oauth2#revoking-a-token

# SECTION: OAuth2 Enhancements
# TODO: Implement token revocation
#       Revoke user tokens securely using Discord's OAuth2 revoke endpoint.
# TODO: Add refresh fallback logic
#       Automatically refresh tokens on expiry and retry failed API calls.






