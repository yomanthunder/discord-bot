# app/main.py
from fastapi import FastAPI
from app.api import interactions
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(interactions.router)
# app.include_router(interactions.router, prefix="/api", tags=["api"])



origins = [
    "http://localhost:5173",
    "https://your-frontend-domain.com"
]

# Configure CORS middleware : change origins as per your frontend domain and during deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def read_root():
    return {"message": "Hello, User!"}