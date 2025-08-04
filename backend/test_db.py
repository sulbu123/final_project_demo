#!/usr/bin/env python3
"""
MariaDB 연결 테스트
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 환경변수 로드
load_dotenv()

def test_database_connection():
    """데이터베이스 연결 테스트"""
    try:
        # 데이터베이스 URL
        database_url = os.getenv("DATABASE_URL")
        print(f"🔗 데이터베이스 URL: {database_url}")
        
        # 엔진 생성
        engine = create_engine(database_url)
        
        # 연결 테스트
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ 데이터베이스 연결 성공! 테스트 결과: {row[0]}")
            
            # 데이터베이스 정보 확인
            result = conn.execute(text("SELECT DATABASE() as current_db"))
            row = result.fetchone()
            print(f"📊 현재 데이터베이스: {row[0]}")
            
            # 테이블 목록 확인
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print(f"📋 현재 테이블 수: {len(tables)}")
            
        return True
        
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MariaDB 연결 테스트 시작...")
    success = test_database_connection()
    
    if success:
        print("🎉 데이터베이스 연결 테스트 성공!")
    else:
        print("💥 데이터베이스 연결 테스트 실패!")
