from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.core.config import settings
from app.api.token_store import save_tokens,get_access_token,get_refresh_token

router = APIRouter()

class CodePayload(BaseModel):
    code: str
class RefreshPayload(BaseModel):
    refresh_token:str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str

@router.post("/discord/code", response_model=TokenResponse)
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

    async with httpx.AsyncClient() as client:
        response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Token exchange failed")
    
    # Hardcoding with userid for testing purpose --> should be async call 
    
    token_data = response.json() # parse json obkect into python dict 
    save_tokens(token_data,user_id="shrish")

    return token_data

@router.post("/discord/refresh")
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


# Reference: https://discord.com/developers/docs/topics/oauth2#revoking-a-token

# SECTION: OAuth2 Enhancements
# TODO: Implement token revocation
#       Revoke user tokens securely using Discord's OAuth2 revoke endpoint.
# TODO: Add refresh fallback logic
#       Automatically refresh tokens on expiry and retry failed API calls.

# SECTION: Bot Authentication Features
# TODO: Add advanced bot authentication
#       Support additional parameters and handle scenarios beyond standard bot scope.





