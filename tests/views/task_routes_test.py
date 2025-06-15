from datetime import date, timedelta

def test_create_task_route(client, auth_token, db):
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
    assert response.status_code == 200
    assert response.json()["title"] == "Via Rota"

def test_get_task_route(client, auth_token):
    created = client.post(
        "/tasks/",
        json={"title": "Get Task", "assigned_to": 1},
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()
    task_id = created["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Get Task"

def test_update_task_route(client, auth_token):
    created = client.post(
        "/tasks/",
        json={"title": "To Update", "assigned_to": 1},
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()
    task_id = created["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Atualizado"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Atualizado"

def test_delete_task_route(client, auth_token):
    created = client.post(
        "/tasks/",
        json={"title": "To Delete", "assigned_to": 1},
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()
    task_id = created["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"

def test_list_tasks_filtered_route(client, auth_token):
    client.post(
        "/tasks/",
        json={
            "title": "Filtro Tarefa",
            "assigned_to": 1,
            "priority": "high",
            "status": "done",
            "due_date": str(date.today() + timedelta(days=1))
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    response = client.get(
        f"/tasks/?status=done&priority=high&dueBefore={str(date.today() + timedelta(days=2))}&assignedTo=1",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert any(t["title"] == "Filtro Tarefa" for t in response.json())
