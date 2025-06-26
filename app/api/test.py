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
print(settings.DISCORD_API_BASE_URL)
print(settings.DISCORD_CLIENT_ID , settings.DISCORD_CLIENT_SECRET, settings.DISCORD_REDIRECT_URI, settings.DISCORD_PUBLIC_KEY, settings.DISCORD_BOT_TOKEN)
# response = httpx.post(f"{settings.DISCORD_API_BASE_URL}/oauth2/token", data=data, headers=headers)
# print(response.status_code)
# print(response.text)
