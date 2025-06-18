import pytest
from fastapi import HTTPException
from src.controllers.comment_controller import create_comment, list_comments, delete_comment
from src.models.comment_model import CommentCreate
from src.models.task_model import Task

@pytest.fixture
def comment_data():
    return CommentCreate(content="Comentário de teste")

@pytest.fixture(autouse=True)
def setup_task(db):
    # Cria uma tarefa para os testes de comentário
    task = Task(
        title="Tarefa de Teste",
        description="Descrição",
        status="pending",
        priority="medium",
        due_date=None,
        assigned_to=None
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def test_create_comment_success(db, comment_data, setup_task):
    comment = create_comment(setup_task.id, 1, comment_data, db)
    assert comment.id is not None
    assert comment.content == comment_data.content
    assert comment.task_id == setup_task.id
    assert comment.user_id == 1

def test_create_comment_task_not_found(db, comment_data):
    with pytest.raises(HTTPException) as exc:
        create_comment(9999, 1, comment_data, db)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Tarefa não encontrada"

def test_list_comments_success(db, setup_task):
    comments = list_comments(setup_task.id, db)
    assert isinstance(comments, list)
    assert comments == []

def test_list_comments_task_not_found(db):
    with pytest.raises(HTTPException) as exc:
        list_comments(9999, db)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Tarefa não encontrada"

def test_delete_comment_success(db, comment_data, setup_task):
    comment = create_comment(setup_task.id, 1, comment_data, db)
    response = delete_comment(comment.id, 1, db)
    assert response == {"message": "Comentário removido com sucesso"}

def test_delete_comment_not_found(db):
    with pytest.raises(HTTPException) as exc:
        delete_comment(9999, 1, db)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Comentário não encontrado"

def test_delete_comment_permission_denied(db, comment_data, setup_task):
    comment = create_comment(setup_task.id, 1, comment_data, db)
    with pytest.raises(HTTPException) as exc:
        delete_comment(comment.id, 2, db)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Permissão negada"
