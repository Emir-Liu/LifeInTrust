"""database operator for task model"""

from uuid import UUID, uuid4
from typing import Optional, List

from sqlalchemy.orm import Session


from .session import with_session
from .task_model import TaskModel

from app.configs import LoggerOperation

logger = LoggerOperation().get_logger("model")


@with_session
def add_task(
    session: Session,
    task_name: str,
    task_id: Optional[UUID] = None,
    parent_task_id: Optional[UUID] = None,
    create_by: Optional[UUID] = None,
) -> UUID:
    """add task

    Args:
        task_name (_type_): _description_
        task_id (_type_): _description_
        parent_task_id (_type_): _description_
        create_by (_type_): _description_
    """

    if task_id is None:
        task_id = uuid4()
    new_task_data = TaskModel(
        name=task_name, parent_task_id=parent_task_id, create_by=create_by, id=task_id
    )
    session.add(new_task_data)

    return task_id


@with_session
def tree_task(
    session: Session,
    task_id: UUID,
    user_id: Optional[UUID] = None,
) -> dict:
    logger.info("task id:%s", task_id)
    if task_id:

        root_task = session.query(TaskModel).filter(TaskModel.id == task_id).first()
        task_tree = root_task.__dict__
        task_tree["child_task"] = list_child_task(task_id=task_id)
        return task_tree
    else:
        root_task = (
            session.query(TaskModel).filter(TaskModel.parent_task_id == None).first()
        )
        task_tree = root_task.__dict__
        task_tree["child_task"] = list_child_task(task_id=root_task.id)
        return task_tree


@with_session
def list_child_task(session: Session, task_id: UUID) -> List[dict]:
    child_tasks = (
        session.query(TaskModel).filter(TaskModel.parent_task_id == task_id).all()
    )

    child_task_list = []
    for tmp_child_task in child_tasks:
        tmp_child_task_list = tmp_child_task.__dict__
        tmp_child_task_list["child_task"] = list_child_task(task_id=tmp_child_task.id)
        child_task_list.append(tmp_child_task_list)
    return child_task_list


@with_session
def delete_task(session: Session, task_id: UUID) -> bool:
    tmp_task_data = session.query(TaskModel).filter(TaskModel.id == task_id).first()

    session.delete(tmp_task_data)

    return True


@with_session
def update_task(
    session: Session,
    task_id: UUID,
    task_name: Optional[str] = None,
    parent_task_id: Optional[UUID] = None,
) -> bool:
    tmp_task_data = session.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task_name:
        tmp_task_data.name = task_name
    if parent_task_id:
        tmp_task_data.parent_task_id = parent_task_id

    return tmp_task_data.__dict__


@with_session
def add_task_root(
    session: Session,
):
    add_task(task_name="RootTask")
