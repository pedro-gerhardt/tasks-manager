from datetime import date, timedelta

def test_create_task_route(client, auth_token):
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
    assert r.status_code == 201  # criação via POST deve ser 201 Created
    body = r.json()
    assert body["title"] == "Via Rota"
    assert "id" in body

def test_get_task_route(client, auth_token):
    crt = client.post(
        "/tasks/",
        json={"title": "Get Task", "assigned_to": 1},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert crt.status_code == 201
    tid = crt.json()["id"]

    r = client.get(f"/tasks/{tid}", headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 200
    assert r.json()["title"] == "Get Task"

def test_update_task_route(client, auth_token):
    crt = client.post("/tasks/", json={"title": "To Update", "assigned_to": 1},
                      headers={"Authorization": f"Bearer {auth_token}"})
    tid = crt.json()["id"]

    r = client.put(
        f"/tasks/{tid}",
        json={"title": "Atualizado"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert r.status_code == 200
    assert r.json()["title"] == "Atualizado"

def test_delete_task_route(client, auth_token):
    crt = client.post("/tasks/", json={"title": "To Delete", "assigned_to": 1},
                      headers={"Authorization": f"Bearer {auth_token}"})
    tid = crt.json()["id"]

    r = client.delete(f"/tasks/{tid}", headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 204  # delete deve ser 204 No Content
    assert r.content == b""

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
    r = client.get(
        f"/tasks/?status=done&priority=high&dueBefore={str(date.today()+timedelta(days=2))}&assignedTo=1",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert r.status_code == 200
    assert any(t["title"] == "Filtro Tarefa" for t in r.json())
