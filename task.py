from mykafka.consumer import kafka_consumer
from myredis.client import redis_client


def get_report():
    """
    获取公司任务完成情况报表，即每个部门所属员工未完成任务的总数量
    :return: dict表示的报表:
    {
        "部门1": {
            "员工1": 1,
            "员工2": 0,
            ...
        },
        "部门2": {
            "员工1": 0,
            "员工2": 2,
            ...
        }
        ...
    }
    """
    # TODO:查询redis员工数据库，遍历库中所有条目即可
    #      本任务管理系统中的员工和普通用户的任务信息分别存储在redis中的两个数据库


def add_task_employee(number, name, department, task):
    """
    给员工添加任务
    :param number: 工号
    :param name: 姓名
    :param department: 部门
    :param task: 任务
    :return: None
    """
    # TODO:在员工对应的redis数据库中添加任务条目，条目格式为:
    #      <number>:{
    #          "name": <name>,
    #          "department": <department>,
    #          "task": [..., <task>],
    #      }


def add_task_non_employee(name, task):
    """
    给普通用户添加任务
    :param name: 姓名
    :param task: 任务
    :return: None
    """
    pass
