import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.api.token_store import get_access_token

router = APIRouter()

# Writing api endpoints for getting User data and guilds

@router.get("/")
async def get_user_data(user_id: str):

    access_token = get_access_token(user_id)
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    headers={
        "Authorization": f"Bearer {access_token}"
    }
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            f"{settings.DISCORD_API_BASE_URL}/users/@me",
            headers=headers
        )

    if user_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user data")

    user_data = user_response.json()
    return user_data

@router.get("/guilds")
async def get_user_guilds(user_id: str):
    access_token = get_access_token(user_id)
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    headers={
        "Authorization": f"Bearer {access_token}"
    }   
    async with httpx.AsyncClient() as client:
        guilds_response = await client.get(
            f"{settings.DISCORD_API_BASE_URL}/users/@me/guilds",
            headers=headers
        )
    if guilds_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user guilds")      
    guilds_data = guilds_response.json()
    filtered_guilds = [guild for guild in guilds_data if guild.get("owner", False)]
    if not filtered_guilds:
        raise HTTPException(status_code=404, detail="No guilds found for the user")
    
    return filtered_guilds