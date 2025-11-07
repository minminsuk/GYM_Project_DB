import os
from pathlib import Path
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import pymysql.cursors
from app.main import app

# 테스트 환경 변수 로드
load_dotenv(Path(__file__).parent / ".env.test")

@pytest.fixture(scope="session")
def test_db():
    """테스트 데이터베이스 연결을 제공하고 테스트 데이터를 설정합니다."""
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    
    # 테스트 데이터 설정
    with connection.cursor() as cursor:
        # 기존 데이터 초기화
        cursor.execute("DELETE FROM checkin_logs")
        cursor.execute("DELETE FROM uniform_rentals")
        cursor.execute("DELETE FROM locker_rentals")
        cursor.execute("DELETE FROM members")
        cursor.execute("DELETE FROM membership_types")
        cursor.execute("DELETE FROM admins")
        
        # 테스트용 관리자 계정 생성
        cursor.execute(
            "INSERT INTO admins (password_hash) VALUES (%s)",
            ("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewcP.h9DIFQxnJgK",)  # 'test1234'의 해시
        )
        
        # 테스트용 회원권 종류 생성
        cursor.execute(
            "INSERT INTO membership_types (name, duration_days) VALUES (%s, %s)",
            ("1개월 회원권", 30)
        )
        
        connection.commit()
    
    yield connection
    
    # 테스트 종료 후 데이터 정리
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM checkin_logs")
        cursor.execute("DELETE FROM uniform_rentals")
        cursor.execute("DELETE FROM locker_rentals")
        cursor.execute("DELETE FROM members")
        cursor.execute("DELETE FROM membership_types")
        cursor.execute("DELETE FROM admins")
        connection.commit()
    
    connection.close()

@pytest.fixture
def client():
    """테스트 클라이언트를 제공합니다."""
    return TestClient(app)

@pytest.fixture
def db_cursor(test_db):
    """테스트용 데이터베이스 커서를 제공합니다."""
    with test_db.cursor() as cursor:
        yield cursor
        test_db.commit()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db():
    """테스트용 DB 연결을 제공하는 fixture"""
    connection = pymysql.connect(
        host='localhost',
        user='root',  # 실제 환경에서는 환경 변수 사용
        password='1234',  # 실제 환경에서는 환경 변수 사용
        db='gym_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # 테스트 전에 필요한 초기 데이터 설정
            yield cursor
    finally:
        connection.close()