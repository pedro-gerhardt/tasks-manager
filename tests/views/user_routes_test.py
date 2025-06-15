from src.models.user_model import UserUpdate

def test_create_user_route(client, auth_token):
    response = client.post(
        "/users/",
        json={
            "name": "João",
            "email": "joao@example.com",
            "password": "joaopass"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "joao@example.com"

def test_get_user_route(client, auth_token):
    # cria usuário
    created = client.post(
        "/users/",
        json={"name": "Lia", "email": "lia@example.com", "password": "xx"},
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()
    user_id = created["id"]

    # busca por ID
    response = client.get(f"/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "lia@example.com"

def test_update_user_route(client, auth_token):
    created = client.post(
        "/users/",
        json={"name": "Bruno", "email": "bruno@example.com", "password": "b"},
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()
    user_id = created["id"]
    print(user_id)
    response = client.put(
        f"/users/{user_id}",
        json={"name": "Bruno Alterado"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    print(response.json())
    assert response.json()["name"] == "Bruno Alterado"

def test_delete_user_route(client, auth_token):
    created = client.post(
        "/users/",
        json={"name": "Paula", "email": "paula@example.com", "password": "p"},
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()
    user_id = created["id"]

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User deactivated"

    # Tenta buscar após soft delete
    get_response = client.get(f"/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert get_response.status_code == 404
