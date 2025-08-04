from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

@app.get("/")
async def root():
    return {"message": "도로 주행 퀴즈 API 서버"}

@app.post("/api/auth/register")
async def register(user: UserCreate):
    return {
        "id": 1,
        "email": user.email,
        "username": user.username,
        "is_active": True
    }

@app.post("/api/auth/login")
async def login(username: str, password: str):
    return {
        "access_token": "test_token_123",
        "token_type": "bearer"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 