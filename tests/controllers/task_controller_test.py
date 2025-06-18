import pytest
from fastapi import HTTPException
from datetime import date, timedelta

from src.controllers.task_controller import (
    create_task,
    get_task,
    list_tasks_by_user,
    update_task,
    delete_task,
    list_tasks_filtered
)
from src.models.task_model import TaskCreate, TaskUpdate

@pytest.fixture(autouse=True)
def ensure_user(db):
    # a fixture clear_and_seed_db já garantiu que o User ID=1 exista
    return

def test_create_and_get_task_direct(db):
    tc = TaskCreate(
        title="Teste 1",
        description="Desc 1",
        assigned_to=1,
        priority="high",
        due_date=date.today() + timedelta(days=7)
    )
    created = create_task(tc, db)
    assert created.id is not None
    assert created.title == tc.title

    fetched = get_task(created.id, db)
    assert fetched.title == "Teste 1"

def test_create_task_invalid_priority(db):
    tc = TaskCreate(title="Tarefa", assigned_to=1, priority="urgent")
    with pytest.raises(HTTPException) as exc:
        create_task(tc, db)
    assert exc.value.status_code == 400
    assert "Prioridade inválida" in exc.value.detail

def test_create_task_invalid_status(db):
    tc = TaskCreate(title="Tarefa", assigned_to=1, status="archived")
    with pytest.raises(HTTPException) as exc:
        create_task(tc, db)
    assert exc.value.status_code == 400
    assert "Status inválido" in exc.value.detail

def test_create_task_due_date_in_past(db):
    past = date.today() - timedelta(days=1)
    tc = TaskCreate(title="Tarefa", assigned_to=1, due_date=past)
    with pytest.raises(HTTPException) as exc:
        create_task(tc, db)
    assert exc.value.status_code == 400
    assert "due_date não pode ser anterior" in exc.value.detail

def test_get_task_not_found(db):
    with pytest.raises(HTTPException) as exc:
        get_task(9999, db)
    assert exc.value.status_code == 404
    assert "Tarefa (ID=9999) não encontrada" in exc.value.detail

def test_list_tasks_by_user(db):
    t1 = TaskCreate(title="A", assigned_to=1)
    t2 = TaskCreate(title="B", assigned_to=1)
    create_task(t1, db)
    create_task(t2, db)
    result = list_tasks_by_user(1, db)
    assert isinstance(result, list)
    assert all(t.assigned_to == 1 for t in result)

def test_list_tasks_by_user_user_not_found(db):
    with pytest.raises(HTTPException) as exc:
        list_tasks_by_user(9999, db)
    assert exc.value.status_code == 404
    assert "Usuário (ID=9999) não encontrado" in exc.value.detail

def test_update_task_direct(db):
    tc = TaskCreate(title="To Update", assigned_to=1)
    created = create_task(tc, db)
    upd = TaskUpdate(title="Updated", priority="low")
    updated = update_task(created.id, upd, db)
    assert updated.title == "Updated"
    assert updated.priority == "low"

def test_update_task_invalid_priority(db):
    created = create_task(TaskCreate(title="X", assigned_to=1), db)
    with pytest.raises(HTTPException) as exc:
        update_task(created.id, TaskUpdate(priority="bad"), db)
    assert exc.value.status_code == 400
    assert "Prioridade inválida" in exc.value.detail

def test_update_task_due_date_in_past(db):
    created = create_task(TaskCreate(title="Y", assigned_to=1), db)
    with pytest.raises(HTTPException) as exc:
        update_task(
            created.id,
            TaskUpdate(due_date=date.today() - timedelta(days=1)),
            db
        )
    assert exc.value.status_code == 400
    assert "due_date não pode ser anterior" in exc.value.detail

def test_delete_task_direct(db):
    created = create_task(TaskCreate(title="Del", assigned_to=1), db)
    resp = delete_task(created.id, db)
    assert resp["message"] == "Tarefa removida com sucesso"
    with pytest.raises(HTTPException) as exc:
        get_task(created.id, db)
    assert exc.value.status_code == 404

def test_list_tasks_filtered_valid_filters(db):
    t1 = TaskCreate(
        title="F1",
        assigned_to=1,
        status="done",
        priority="medium",
        due_date=date.today() + timedelta(days=3)
    )
    t2 = TaskCreate(
        title="F2",
        assigned_to=1,
        status="done",
        priority="high",
        due_date=date.today() + timedelta(days=1)
    )
    create_task(t1, db)
    create_task(t2, db)
    filtered = list_tasks_filtered(
        db,
        status_filter="done",
        priority="high",
        due_before=date.today() + timedelta(days=2),
        user_id=1
    )
    assert any(t.title == "F2" for t in filtered)

def test_list_tasks_filtered_invalid_params(db):
    with pytest.raises(HTTPException) as exc:
        list_tasks_filtered(db, status_filter=None, priority="urgent")
    assert exc.value.status_code == 400
    assert "Prioridade inválida" in exc.value.detail
