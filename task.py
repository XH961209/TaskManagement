import threading
import time
from mykafka.consumer import kafka_consumer
from myredis.client import redis_client
from common import TASK_UPDATE_PASSWORD


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


def add_task(number, name, department, task):
    """
    给用户添加任务
    :param number: 工号
    :param name: 姓名
    :param department: 部门
    :param task: 任务，字符串类型
    :return: None
    """
    content = {
        "name": name,
        "department": department,
        "tasks": task + "#0"
    }
    if redis_client.hgetall(number) == {}:
        # 任务管理系统中还不存在该用户的信息，添加
        redis_client.hset(name=number, mapping=content)
    else:
        # 任务管理系统中已经存在该用户信息，在该用户任务栏添加任务
        old_tasks = redis_client.hget(name=number, key="tasks").decode()
        new_tasks = old_tasks + "|" + task + "#0"
        redis_client.hset(name=number, key="tasks", value=new_tasks)


def change_task_state(tasks, task, state):
    """
    改变某一任务的状态
    :param tasks: 所有任务
    :param task: 指定任务
    :param state: 目标状态
    :return: 改变后的tasks
    """
    tasks = tasks.split('|')
    new_tasks = []
    for cur_task in tasks:
        task_name = cur_task.split('#')[0]
        if task_name == task:
            new_tasks.append(task_name + "#{}".format(state))
        else:
            new_tasks.append(cur_task)
    return "|".join(new_tasks)


def consume_kafka():
    """
    从kafka中消费用户管理系统发来的消息
    :return:
    """
    while True:
        tp_to_records = kafka_consumer.poll()
        kafka_consumer.commit()
        for tp in tp_to_records:
            records = tp_to_records[tp]
            for record in records:
                msg = record.value.decode()
                msg_slices = msg.split('|')
                if msg_slices[0] == "new user":
                    number = msg_slices[1]
                    name = msg_slices[2]
                    department = msg_slices[3]
                    add_task(number, name, department, TASK_UPDATE_PASSWORD)
                elif msg_slices[0] == "update password":
                    number = msg_slices[1]
                    tasks = redis_client.hget(number, "tasks").decode()
                    tasks = change_task_state(tasks, TASK_UPDATE_PASSWORD, "1")
                    redis_client.hset(name=number, key="tasks", value=tasks)
                else:
                    # TODO:打印log
                    pass
        time.sleep(1)


if __name__ == "__main__":
    consume_threading = threading.Thread(target=consume_kafka, name="ConsumeThreading")
    consume_threading.start()
