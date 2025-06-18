def test_create_user_route(client, auth_token):
    r = client.post(
        "/users/",
        json={"name":"João","email":"joao@example.com","password":"joaopass"},
        headers={"Authorization":f"Bearer {auth_token}"}
    )
    assert r.status_code == 201  # criação deve retornar 201
    data = r.json()
    assert data["email"] == "joao@example.com"
    assert "id" in data

def test_get_user_route(client, auth_token):
    cr = client.post(
        "/users/",
        json={"name":"Lia","email":"lia@example.com","password":"xxxx"},
        headers={"Authorization":f"Bearer {auth_token}"}
    )
    assert cr.status_code == 201
    uid = cr.json()["id"]

    r = client.get(f"/users/{uid}", headers={"Authorization":f"Bearer {auth_token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "lia@example.com"

def test_update_user_route(client, auth_token):
    cr = client.post(
        "/users/",
        json={"name":"Bruno","email":"bruno@example.com","password":"bbbb"},
        headers={"Authorization":f"Bearer {auth_token}"}
    )
    assert cr.status_code == 201
    uid = cr.json()["id"]

    r = client.put(
        f"/users/{uid}",
        json={"name":"Bruno Alterado"},
        headers={"Authorization":f"Bearer {auth_token}"}
    )
    assert r.status_code == 200
    assert r.json()["name"] == "Bruno Alterado"

def test_delete_user_route(client, auth_token):
    cr = client.post(
        "/users/",
        json={"name":"Paula","email":"paula@example.com","password":"pppp"},
        headers={"Authorization":f"Bearer {auth_token}"}
    )
    assert cr.status_code == 201
    uid = cr.json()["id"]

    r = client.delete(f"/users/{uid}", headers={"Authorization":f"Bearer {auth_token}"})
    assert r.status_code == 204
    assert r.content == b""

    r2 = client.get(f"/users/{uid}", headers={"Authorization":f"Bearer {auth_token}"})
    assert r2.status_code == 404
