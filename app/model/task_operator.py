"""database operator for task model"""

from uuid import UUID, uuid4
from typing import Optional, List
from datetime import datetime
from copy import deepcopy

from sqlalchemy.orm import Session


from .session import with_session
from .task_model import TaskModel

from app.configs import LoggerOperation, ROOT_TASK_NAME

logger = LoggerOperation().get_logger("model")


@with_session
def add_task(
    session: Session,
    task_name: str,
    task_id: Optional[UUID] = None,
    parent_task_id: Optional[UUID] = None,
    create_by: Optional[UUID] = None,
    order: int = -1,
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

    # change order
    tmp_task_list = (
        session.query(TaskModel)
        .filter(
            TaskModel.parent_task_id == parent_task_id, TaskModel.create_by == create_by
        )
        .order_by(TaskModel.order)
        .all()
    )
    if order == -1 or order >= len(tmp_task_list):
        order = len(tmp_task_list)
    else:
        for tmp_task in tmp_task_list:
            if tmp_task.order >= order:
                tmp_task.order += 1
    new_task_data = TaskModel(
        name=task_name,
        parent_task_id=parent_task_id,
        create_by=create_by,
        id=task_id,
        order=order,
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
    else:
        root_task = (
            session.query(TaskModel).filter(TaskModel.parent_task_id == None).first()
        )
    task_tree = root_task.__dict__
    task_tree["child_task"] = list_child_task(task_id=root_task.id)
    logger.info("task_tree:%s", task_tree)
    return task_tree


@with_session
def list_child_task(
    session: Session, task_id: UUID, bool_recursion: bool = True
) -> List[dict]:
    child_tasks = (
        session.query(TaskModel).filter(TaskModel.parent_task_id == task_id).all()
    )

    child_task_list = []
    for tmp_child_task in child_tasks:
        tmp_child_task_list = tmp_child_task.__dict__
        if bool_recursion is True:
            tmp_child_task_list["child_task"] = list_child_task(
                task_id=tmp_child_task.id
            )
            tmp_child_task_list["parent_task_id"] = task_id
        else:
            pass
        child_task_list.append(tmp_child_task_list)
    return child_task_list


@with_session
def delete_task(session: Session, task_id: UUID) -> bool:
    tmp_task_data = session.query(TaskModel).filter(TaskModel.id == task_id).first()
    tmp_task_list = (
        session.query(TaskModel)
        .filter(TaskModel.parent_task_id == tmp_task_data.parent_task_id)
        .order_by(TaskModel.order)
        .all()
    )

    for tmp_task in tmp_task_list:
        if tmp_task.order > tmp_task_data.order:
            tmp_task.order -= 1
    session.delete(tmp_task_data)

    return True


def trans_datetime2str(time: datetime):
    """将datetime格式数据转换为str格式数据

    Args:
        time (datetime): datetime格式数据
    """

    if isinstance(time, str):
        return time
    elif isinstance(time, datetime):
        formatted_date = time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date


@with_session
def update_task(
    session: Session,
    task_id: UUID,
    task_name: Optional[str] = None,
    parent_task_id: Optional[UUID] = None,
    order: Optional[int] = None,
) -> bool:
    tmp_task_data = session.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task_name:
        tmp_task_data.name = task_name
    if parent_task_id:
        tmp_task_data.parent_task_id = parent_task_id


    # print("update info: %s", tmp_task_data.__dict__)
    # return True

    # work
    ret_dict = {}

    for key, val in deepcopy(tmp_task_data.__dict__).items():
        logger.info("key: %s val: %s type: %s", key, val, type(val))
        if "_" in key:
            continue
        elif isinstance(val, UUID):
            ret_dict[key] = str(val)
        elif isinstance(val, datetime):
            ret_dict[key] = trans_datetime2str(val)
        ret_dict[key] = val
    return ret_dict


    # return tmp_task_data.__dict__

# home
@with_session
def add_task_root(
    session: Session,
):
    add_task(task_name=ROOT_TASK_NAME)


@with_session
def get_taskid_by_name(
    session: Session,
    task_name: str,
):
    task_info = session.query(TaskModel).filter(TaskModel.name == task_name).first()
    if task_info:
        return task_info.id
    return None
