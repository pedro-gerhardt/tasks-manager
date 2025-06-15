import pytest
from src.models.comment_model import CommentCreate
from src.controllers import comment_controller

@pytest.fixture
def comment_data():
    return CommentCreate(content="Comentário de teste")

def test_create_comment(db, comment_data):
    task_id = 1
    user_id = 1
    comment = comment_controller.create_comment(task_id, user_id, comment_data, db)

    assert comment.id is not None
    assert comment.content == comment_data.content
    assert comment.task_id == task_id
    assert comment.user_id == user_id

def test_list_comments(db):
    task_id = 1
    comments = comment_controller.list_comments(task_id, db)
    assert isinstance(comments, list)

def test_delete_comment(db, comment_data):
    task_id = 1
    user_id = 1
    comment = comment_controller.create_comment(task_id, user_id, comment_data, db)

    response = comment_controller.delete_comment(comment.id, user_id, db)
    assert response == {"message": "Comment deleted"}

    with pytest.raises(Exception) as e:
        comment_controller.delete_comment(999999, user_id, db)
    assert "not found" in str(e.value)

    comment = comment_controller.create_comment(task_id, user_id, comment_data, db)
    with pytest.raises(Exception) as e:
        comment_controller.delete_comment(comment.id, user_id + 1, db) 
    assert "only delete your own" in str(e.value)
