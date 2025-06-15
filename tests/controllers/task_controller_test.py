from src.controllers import task_controller
from src.models.task_model import TaskCreate, TaskUpdate
from fastapi import HTTPException
from datetime import date, timedelta

def test_create_and_get_task_direct(db):
    task = TaskCreate(
        title="Teste 1",
        description="Desc 1",
        assigned_to=1,
        priority="high",
        due_date=date.today() + timedelta(days=7)
    )
    created = task_controller.create_task(task, db)
    assert created.id is not None
    assert created.title == task.title

    fetched = task_controller.get_task(created.id, db)
    assert fetched.title == "Teste 1"

def test_update_task_direct(db):
    task = TaskCreate(title="To Update", assigned_to=1)
    created = task_controller.create_task(task, db)
    
    updated_data = TaskUpdate(title="Updated Title", priority="low")
    updated = task_controller.update_task(created.id, updated_data, db)

    assert updated.title == "Updated Title"
    assert updated.priority == "low"

def test_delete_task_direct(db):
    task = TaskCreate(title="To Delete", assigned_to=1)
    created = task_controller.create_task(task, db)

    result = task_controller.delete_task(created.id, db)
    assert result["message"] == "Task deleted"

    try:
        task_controller.get_task(created.id, db)
        assert False, "Deveria lançar erro 404"
    except HTTPException as e:
        assert e.status_code == 404

def test_list_tasks_by_user(db):
    task1 = TaskCreate(title="Tarefa A", assigned_to=1)
    task2 = TaskCreate(title="Tarefa B", assigned_to=1)
    task_controller.create_task(task1, db)
    task_controller.create_task(task2, db)

    task3 = TaskCreate(title="Tarefa C", assigned_to=2)
    task_controller.create_task(task3, db)

    result = task_controller.list_tasks_by_user(1, db)
    assert isinstance(result, list)
    assert all(t.assigned_to == 1 for t in result)
    titles = [t.title for t in result]
    assert "Tarefa A" in titles
    assert "Tarefa B" in titles
    assert "Tarefa C" not in titles


def test_list_tasks_filtered_direct(db):
    task1 = TaskCreate(
        title="Filter1",
        assigned_to=1,
        status="done",
        priority="medium",
        due_date=date.today() + timedelta(days=3)
    )
    task2 = TaskCreate(
        title="Filter2",
        assigned_to=1,
        status="done",
        priority="high",
        due_date=date.today() + timedelta(days=1)
    )
    task_controller.create_task(task1, db)
    task_controller.create_task(task2, db)

    filtered = task_controller.list_tasks_filtered(
        db,
        status="done",
        priority="high",
        due_before=date.today() + timedelta(days=2),
        user_id=1, 
    )
    assert any(t.title == "Filter2" for t in filtered)
