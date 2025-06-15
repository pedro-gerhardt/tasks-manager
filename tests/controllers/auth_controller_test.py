from src.controllers.auth_controller import login_user
from src.models.user_model import UserLogin
from fastapi import HTTPException

def test_login_user_success(create_test_user):
    credentials = UserLogin(email=create_test_user.email, password="1234")
    response = login_user(credentials)
    assert "access_token" in response
    assert response["token_type"] == "bearer"

def test_login_user_wrong_password(create_test_user):
    credentials = UserLogin(email=create_test_user.email, password="wrong")
    try:
        login_user(credentials)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 401
        assert e.detail == "Invalid credentials"

def test_login_user_email_not_found():
    credentials = UserLogin(email="naoexiste@teste.com", password="123")
    try:
        login_user(credentials)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 401
        assert e.detail == "Invalid credentials"
