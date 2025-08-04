#!/usr/bin/env python3
"""
모델 테스트
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, UserStats

# 환경변수 로드
load_dotenv()

def test_models():
    """모델 테스트"""
    try:
        # 데이터베이스 URL
        database_url = os.getenv("DATABASE_URL")
        print(f"🔗 데이터베이스 URL: {database_url}")
        
        # 엔진 생성
        engine = create_engine(database_url)
        
        # 테이블 생성
        Base.metadata.create_all(bind=engine)
        print("✅ 테이블 생성 완료!")
        
        # 세션 생성
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # 테스트 사용자 생성
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="test_hash"
        )
        db.add(test_user)
        db.commit()
        print(f"✅ 테스트 사용자 생성 완료! ID: {test_user.id}")
        
        # 사용자 통계 생성
        user_stats = UserStats(
            user_id=test_user.id,
            total_quizzes=0,
            correct_answers=0,
            streak=0,
            level="초급",
            points=0
        )
        db.add(user_stats)
        db.commit()
        print(f"✅ 사용자 통계 생성 완료! ID: {user_stats.id}")
        
        # 테이블 목록 확인
        result = db.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"📋 생성된 테이블: {[table[0] for table in tables]}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 모델 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("🚀 모델 테스트 시작...")
    success = test_models()
    
    if success:
        print("🎉 모델 테스트 성공!")
    else:
        print("💥 모델 테스트 실패!") 