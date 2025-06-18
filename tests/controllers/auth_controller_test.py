from src.controllers.auth_controller import login_user
from src.models.user_model import UserLogin
from fastapi import HTTPException

def test_login_user_success(create_test_user, db):
    credentials = UserLogin(email=create_test_user.email, password="1234")
    response = login_user(credentials, db)
    assert "access_token" in response
    assert response["token_type"] == "bearer"

def test_login_user_wrong_password(create_test_user, db):
    credentials = UserLogin(email=create_test_user.email, password="wrongpass")
    try:
        login_user(credentials, db)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 401
        assert e.detail == "Credenciais inválidas"  # conforme auth_controller.py :contentReference[oaicite:0]{index=0}

def test_login_user_email_not_found(db):
    credentials = UserLogin(email="noone@nowhere.com", password="1234")
    try:
        login_user(credentials, db)
        assert False, "Expected HTTPException"
    except HTTPException as e:
        assert e.status_code == 401
        assert e.detail == "Credenciais inválidas"  # idem :contentReference[oaicite:1]{index=1}
