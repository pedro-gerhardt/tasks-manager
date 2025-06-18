import pytest
from datetime import date, timedelta

@pytest.fixture(scope="function")
def task(client, auth_token):
    r = client.post(
        "/tasks/",
        json={
            "title": "Via Rota",
            "description": "Teste",
            "assigned_to": 1,
            "priority": "high",
            "due_date": str(date.today() + timedelta(days=5))
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert r.status_code == 201
    return r.json()

def test_add_comment_route(client, auth_token, task):
    r = client.post(
        f"/tasks/{task['id']}/comments",
        json={"content": "Comentário via rota"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert r.status_code == 201  # conforme comment_routes.post :contentReference[oaicite:5]{index=5}
    assert r.json()["content"] == "Comentário via rota"

def test_get_comments_route(client, auth_token, task):
    r = client.get(
        f"/tasks/{task['id']}/comments",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_delete_comment_route(client, auth_token, task):
    # cria 1 comentário
    r1 = client.post(
        f"/tasks/{task['id']}/comments",
        json={"content": "Para deletar"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    comment = r1.json()

    r2 = client.delete(
        f"/tasks/{task['id']}/comments/{comment['id']}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert r2.status_code == 204  # conforme comment_routes.delete :contentReference[oaicite:6]{index=6}
    assert r2.content == b""
