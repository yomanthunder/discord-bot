import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import settings
from app.services.token_store import get_access_token,get_valid_access_token
from app.services.token_store import save_user
router = APIRouter()

# Writing api endpoints for getting User data and guilds
class UserRequest(BaseModel):
    user_id: str

@router.post("/")
async def get_user_data(request: UserRequest):
    user_id = request.user_id
    token = await get_valid_access_token(user_id)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    headers={
        "Authorization": f"Bearer {token.access_token}" # type: ignore
    }
    try:
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                f"{settings.DISCORD_API_BASE_URL}/users/@me",
                headers=headers
            )
        if user_response.status_code != 200:
            print(f"Discord API Error: {user_response.status_code}")
            print(f"Response: {user_response.text}")
            raise HTTPException(
                status_code=user_response.status_code, 
                detail=f"Discord API error: {user_response.text}"
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    
    try:
        # save user in redis if it doesn't exist
        await save_user(user_id=user_id, user_data=user_response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving user data: {str(e)}")

    user_data = user_response.json()
    return user_data

@router.post("/guilds")
async def get_user_guilds(request: UserRequest):
    user_id = request.user_id
    token = await get_valid_access_token(user_id)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    headers={
        "Authorization": f"Bearer {token.access_token}"  # type: ignore
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