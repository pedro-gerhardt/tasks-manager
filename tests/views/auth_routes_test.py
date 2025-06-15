def test_login_success(client, create_test_user):
    response = client.post("/auth/login", json={
        "email": create_test_user.email,
        "password": "1234"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(client, create_test_user):
    response = client.post("/auth/login", json={
        "email": create_test_user.email,
        "password": "wrong-password"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_nonexistent_email(client):
    response = client.post("/auth/login", json={
        "email": "notfound@example.com",
        "password": "1234"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful (stateless JWT - handled client-side)"}
