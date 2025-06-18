def test_login_success(client, create_test_user):
    r = client.post("/auth/login", json={
        "email": create_test_user.email,
        "password": "1234"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_invalid_password(client, create_test_user):
    r = client.post("/auth/login", json={
        "email": create_test_user.email,
        "password": "wrongpass"
    })
    assert r.status_code == 401
    assert r.json()["detail"] == "Credenciais inválidas"  # alinhar com auth_controller :contentReference[oaicite:2]{index=2}

def test_login_nonexistent_email(client):
    r = client.post("/auth/login", json={
        "email": "noone@nowhere.com",
        "password": "1234"
    })
    assert r.status_code == 401
    assert r.json()["detail"] == "Credenciais inválidas"  # idem :contentReference[oaicite:3]{index=3}

def test_logout(client):
    r = client.post("/auth/logout")
    assert r.status_code == 200
    assert r.json() == {"message": "Logout realizado com sucesso"}  # conforme auth_controller.logout_user :contentReference[oaicite:4]{index=4}
