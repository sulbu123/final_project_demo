from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

from app.database import get_db, engine
from app.models import Base
from app.routers import auth, quiz, analysis, user
from app.core.config import settings

# 환경 변수 로드
load_dotenv()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="도로 주행 퀴즈 API",
    description="AI 기반 도로 주행 영상 분석 및 퀴즈 생성 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React 프론트엔드
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["인증"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["퀴즈"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["분석"])
app.include_router(user.router, prefix="/api/user", tags=["사용자"])

@app.get("/")
async def root():
    return {"message": "도로 주행 퀴즈 API 서버"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 