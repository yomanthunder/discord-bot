# from app.api.token_store import save_tokens, get_access_token
# from datetime import datetime 
# from app.core.config import settings
# Save tokens
# token_data = {
#   "access_token": "6qrZcUqja7812RVdnEKjpzOL4CvHBFG",
#   "token_type": "Bearer",
#   "expires_in": 604800,
#   "refresh_token": "D43f5y0ahjqew82jZ4NViEr2YafMKhue",
#   "scope": "identify"
# }
# save_tokens(token_data,user_id="shrish")

# # Get access token later
# token = get_access_token("shrish")
# print(token,datetime.now())

# import asyncio
# import websockets
# import json

# DISCORD_GATEWAY = "wss://gateway.discord.gg/?v=10&encoding=json"

# async def connect():
#     async with websockets.connect(DISCORD_GATEWAY) as websocket:
#         # Receive Hello payload
#         hello_payload = await websocket.recv()
#         print("Received Hello:", hello_payload)

#         # Identify payload — REQUIRED to authenticate with the Discord Gateway
#         identify_payload = {
#             "op": 2,
#             "d": {
#                 "token": settings.DISCORD_BOT_TOKEN,  # Replace with your bot token
#                 "intents": 513,
#                 "properties": {
#                     "$os": "linux",
#                     "$browser": "my_library",
#                     "$device": "my_library"
#                 }
#             }
#         }

#         await websocket.send(json.dumps(identify_payload))
#         print("Sent Identify payload")

#         # Listen for events
#         while True:
#             response = await websocket.recv()
#             print("Event Received:", json.loads(response))

# asyncio.run(connect())

import httpx
from app.core.config import settings
data = {
    "client_id": "1374637794927972412",
    "client_secret": "MV1m7Nv6URBlIZEw_0r1P0NIJRNakE6U",
    "grant_type": "authorization_code",
    "code": "AHB5NaoJx9gYDLiSSrVJpdbiIGZqfs",
    "redirect_uri": "http://localhost:5173/callback"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# response = httpx.post(f"{settings.DISCORD_API_BASE_URL}/oauth2/token", data=data, headers=headers)
# print(response.status_code)
# print(response.text)

# @router.post("/code")
# async def exchange_code(payload: CodePayload):
#     data = {
#         "client_id": settings.DISCORD_CLIENT_ID,
#         "client_secret": settings.DISCORD_CLIENT_SECRET,
#         "grant_type": "authorization_code",
#         "code": payload.code,
#         "redirect_uri": settings.DISCORD_REDIRECT_URI,
#     }

#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     # change the order of calls when cookies are implemented
#     # to get user_id from cookies and then save the tokens
#     async with httpx.AsyncClient() as client:
#         response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)

#     if response.status_code != 200:
#         print("Discord token exchange failed:", response.status_code, response.text)
#         raise HTTPException(status_code=400, detail="Token exchange failed")
#     token_data = response.json()

#     async with httpx.AsyncClient() as client:
#         user_response = await client.get(
#             "https://discord.com/api/users/@me",
#             headers={
#                 "Authorization": f"Bearer {token_data['access_token']}"
#             }
#         )
#     if user_response.status_code != 200:
#         raise HTTPException(status_code=400, detail="Failed to fetch user data")
    
#     # user_data = user_response.json()
#     # session_token = str(uuid.uuid4())
    

#     # save_tokens(token_data, user_id=user_data["id"])
#     # save_user(user_data,user_data["id"])
#     # save_session(user_data, session_token)

#     return token_data


# from app.core.redis_client import redis_client

# key = "user:1377242011375239248:token"

# print("Ping:", redis_client.ping())
# print("Exists:", redis_client.exists(key))
# print("Type:", redis_client.type(key))
# print("HGETALL:", redis_client.hgetall(key))
# print("All Keys:", redis_client.keys("user:*"))

# from pydantic import BaseModel

# class User(BaseModel):
#     id: int
#     name: str
#     email: str

# user_data = User(id=1, name="Alice", email="alice@example.com")
# print(user_data)
# json_string = user_data.model_dump_json()
# print(json_string)

# # deserialized_user = User.model_validate_json(json_string)

# deserialized_user = User.model_validate_json(json_string)
# print(deserialized_user)