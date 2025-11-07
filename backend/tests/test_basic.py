import pytest
from datetime import datetime, timedelta

def test_server_status(client):
    """서버 상태 확인 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"

@pytest.mark.parametrize("test_id, status_code, has_error", [
    ("valid", 200, False),
    ("invalid", 401, True)
])
def test_admin_login(client, test_id, status_code, has_error):
    """관리자 로그인 테스트"""
    test_cases = {
        "valid": {"password": "1234"},
        "invalid": {"password": "wrong"}
    }
    
    response = client.post(
        "/api/admin/login",
        params=test_cases[test_id]
    )
    assert response.status_code == status_code
    data = response.json()
    if not has_error:
        assert data["status"] == "success"
        assert data["message"] == "인증 성공"
    else:
        assert "detail" in data

def test_api_documentation(client):
    """API 문서 접근성 테스트"""
    # Swagger UI
    response = client.get("/api/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # ReDoc
    response = client.get("/api/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # OpenAPI 스키마
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    schema = response.json()
    assert "paths" in schema
    assert "components" in schema