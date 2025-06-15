import pytest
from datetime import date, timedelta

@pytest.fixture(scope="session")
def task(client, auth_token):
    response = client.post(
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
    return response.json()

def test_add_comment_route(client, auth_token, task):
    response = client.post(
        f"/tasks/{task['id']}/comments",
        json={"content": "Comentário via rota"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Comentário via rota"

def test_get_comments_route(client, auth_token, task):
    response = client.get(f"/tasks/{task['id']}/comments", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_comment_route(client, auth_token, task):
    response = client.post(
        f"/tasks/{task['id']}/comments",
        json={"content": "Comentário via rota"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    comment = response.json()
    print(comment)

    response = client.delete(f"/tasks/{task['id']}/comments/{comment['id']}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Comment deleted"}
