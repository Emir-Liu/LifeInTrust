"""task route """

from copy import deepcopy
from fastapi import APIRouter
from typing import Optional

from .util import logger
from app.model import task_operator
from app.model.database_operator import trans_str2uuid

from .util import ret_json

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/add/")
async def add_task(
    task_name: str,
    parent_task_id: Optional[str] = None,
    user_id: Optional[str] = None,
    relation_type: Optional[str] = None,
):
    """add task api

    Args:
        add_task_item (AddTaskItem): _description_

    Returns:
        _type_: _description_
    """
    logger.info("use add task api")
    parent_task_id = trans_str2uuid(parent_task_id)
    user_id = trans_str2uuid(user_id)

    task_id = task_operator.add_task(
        task_name=task_name,
        parent_task_id=parent_task_id,
        create_by=user_id,
    )
    tmp_ret_json = deepcopy(ret_json)
    tmp_ret_json["msg"] = "add task success"
    tmp_ret_json["task_id"] = task_id

    return tmp_ret_json


@router.get("/list/")
async def list_task(task_id: str, user_id: Optional[str] = None):
    """list task tree

    Args:
        task_id (Optional[str], optional): root task id. Defaults to None.
        user_id (Optional[str], optional): user id. Defaults to None.
    """
    logger.info("use list task api")
    task_id = trans_str2uuid(task_id)
    user_id = trans_str2uuid(user_id)

    # if task_id is None and user_id is None:
    #     tmp_ret_json = deepcopy(ret_json)
    #     tmp_ret_json["msg"] = "no input"
    #     tmp_ret_json["task_tree"] = {}
    # else:
    task_tree = task_operator.tree_task(task_id=task_id, user_id=user_id)
    tmp_ret_json = deepcopy(ret_json)
    tmp_ret_json["msg"] = "list task success"
    tmp_ret_json["task_tree"] = task_tree

    return tmp_ret_json


@router.get("/update/")
async def update_task(
    task_id: str, task_name: Optional[str] = None, parent_task_id: Optional[str] = None
) -> dict:
    """update task api

    Args:
        task_id (str): task id
        task_name (Optional[str], optional): task name channge to. Defaults to None.
        parent_task_id (Optional[str], optional): parent task id change to. Defaults to None.

    Returns:
        _type_: dict
    """
    logger.info("use update task api")
    task_id = trans_str2uuid(task_id)
    parent_task_id = trans_str2uuid(parent_task_id)
    new_task = task_operator.update_task(
        task_id=task_id, task_name=task_name, parent_task_id=parent_task_id
    )
    tmp_ret_json = deepcopy(ret_json)
    tmp_ret_json["msg"] = "update task success"
    tmp_ret_json["new_task_info"] = new_task
    return tmp_ret_json


@router.get("/delete")
async def delete_task(task_id: str) -> dict:
    """delete task api

    Args:
        task_id (str): task id

    Returns:
        _type_: dict
    """
    logger.info("use delete task api")
    task_id = trans_str2uuid(task_id)
    task_operator.delete_task(task_id=task_id)
    tmp_ret_json = deepcopy(ret_json)
    tmp_ret_json["msg"] = "delete task success"
    return tmp_ret_json
