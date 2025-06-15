from src.controllers import user_controller
from src.models.user_model import UserCreate, UserUpdate
from fastapi import HTTPException

def test_create_user_direct(db):
    user = UserCreate(name="Maria", email="maria@example.com", password="secret")
    result = user_controller.create_user(user)
    assert result.email == user.email
    assert result.id is not None

def test_get_user_direct(db):
    user = UserCreate(name="Carlos", email="carlos@example.com", password="1234")
    created = user_controller.create_user(user)
    fetched = user_controller.get_user(created.id)
    assert fetched.email == "carlos@example.com"

def test_update_user_direct(db):
    user = UserCreate(name="Laura", email="laura@example.com", password="abc")
    created = user_controller.create_user(user)
    updated_data = UserUpdate(name="Laura Nova")
    updated = user_controller.update_user(created.id, updated_data)
    assert updated.name == "Laura Nova"

def test_delete_user_direct(db):
    user = UserCreate(name="Ana", email="ana@example.com", password="x")
    created = user_controller.create_user(user)
    result = user_controller.delete_user(created.id)
    assert result["message"] == "User deactivated"
    try:
        user_controller.get_user(created.id)
        assert False, "Deveria lançar exceção para usuário desativado"
    except HTTPException as e:
        assert e.status_code == 404
