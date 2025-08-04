#!/usr/bin/env python3
"""
MariaDB 데이터베이스 초기화 스크립트
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.database import engine
from app.models import Base
from app.core.config import settings

def init_database():
    """데이터베이스 초기화"""
    try:
        # 데이터베이스 연결 테스트
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ MariaDB 연결 성공!")
        
        # 테이블 생성
        Base.metadata.create_all(bind=engine)
        print("✅ 데이터베이스 테이블 생성 완료!")
        
        # 초기 데이터 삽입 (선택사항)
        # insert_initial_data()
        
        print("🎉 데이터베이스 초기화 완료!")
        
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")
        sys.exit(1)

def insert_initial_data():
    """초기 데이터 삽입"""
    from sqlalchemy.orm import sessionmaker
    from app.models import User, UserStats
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 테스트 사용자 생성
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gS.Oi"  # password: test123
        )
        db.add(test_user)
        db.commit()
        
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
        
        print("✅ 초기 데이터 삽입 완료!")
        
    except Exception as e:
        print(f"❌ 초기 데이터 삽입 실패: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 MariaDB 데이터베이스 초기화 시작...")
    init_database() 