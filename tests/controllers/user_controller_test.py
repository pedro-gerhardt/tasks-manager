import pytest
from fastapi import HTTPException
from src.controllers.user_controller import create_user, get_user, update_user, delete_user
from src.models.user_model import UserCreate, UserUpdate

def test_create_user_direct(db):
    u = UserCreate(name="Maria", email="maria@example.com", password="secret")
    result = create_user(u, db)
    assert result.email == u.email
    assert result.id is not None

def test_create_user_duplicate_email(db):
    u1 = UserCreate(name="João", email="joao@test.com", password="pass123")
    create_user(u1, db)
    with pytest.raises(HTTPException) as exc:
        create_user(u1, db)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Email já cadastrado"

def test_get_user_direct(db):
    u = UserCreate(name="Carlos", email="carlos@example.com", password="1234")
    created = create_user(u, db)
    fetched = get_user(created.id, db)
    assert fetched.email == "carlos@example.com"

def test_get_user_not_found(db):
    with pytest.raises(HTTPException) as exc:
        get_user(9999, db)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuário não encontrado"

def test_update_user_direct(db):
    u = UserCreate(name="Laura", email="laura@example.com", password="abc123")
    created = create_user(u, db)
    upd = UserUpdate(name="Laura Nova")
    updated = update_user(created.id, upd, db)
    assert updated.name == "Laura Nova"

def test_update_user_not_found(db):
    upd = UserUpdate(name="Não Existe")
    with pytest.raises(HTTPException) as exc:
        update_user(9999, upd, db)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuário não encontrado"

def test_update_user_duplicate_email(db):
    u1 = UserCreate(name="User1", email="user1@test.com", password="pass123")
    u2 = UserCreate(name="User2", email="user2@test.com", password="pass123")
    created1 = create_user(u1, db)
    created2 = create_user(u2, db)
    upd = UserUpdate(email="user1@test.com")
    with pytest.raises(HTTPException) as exc:
        update_user(created2.id, upd, db)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Email já em uso"

def test_delete_user_direct(db):
    u = UserCreate(name="Ana", email="ana@example.com", password="xpass")
    created = create_user(u, db)
    result = delete_user(created.id, db)
    assert result["message"] == "Usuário desativado com sucesso"
    with pytest.raises(HTTPException) as exc:
        get_user(created.id, db)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuário não encontrado"
