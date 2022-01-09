import time
import threading
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from myredis.client import redis_client
from mykafka.consumer import kafka_consumer

app = Flask(__name__)
# 此部分Redis数据库设计如下，员工和普通用户共用同一个表，普通用户的部门类型为""(空字符串)
# key: [name:department]
# value(Hash): { task1: 1 if finished else 0,
#                task2: 1 if finished else 0,
#                ...
#               }


@app.route('/task/api/get_report', methods=['POST'])
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
    report = dict()
    departments = redis_client.smembers("departments")
    for dpt in departments:
        dpt = dpt.decode()
        
        # 查找部门dpt下所有员工的任务记录
        employees = redis_client.keys("*:{}".format(dpt))
        # 如果此部门不存在任务记录，就不统计报表
        if len(employees) == 0: 
            continue

        # total_finished = 0
        total_task = 0
        report[dpt] = dict()
        for emp in employees:
            emp = emp.decode()
            emp_name = emp.split(":")[0]
            report[dpt][emp_name] = redis_client.hlen(emp)
            # for finished in redis_client.hvals(emp):
            #     total_finished += finished.decode()
            total_task += redis_client.hlen(emp)
        report[dpt]['total'] = total_task

    return report


@app.route('/task/api/get_tasks', methods=['POST'])
def get_report():
    """
    TODO: 获取用户任务列表
    :return: dict表示的任务列表:
    {
        "任务1": 0/1是否完成,
        "任务2": 0/1是否完成,
        ...
    }
    """
    pass
    

def add_task_employee(number, department, task):
    """
    给员工添加任务
    :param number: 工号
    :param department: 部门
    :param task: 任务
    :return: None
    """
    key = "{}:{}".format(number, department)
    value = {
        task: 0,
    }
    redis_client.hset(name=key, mapping=value)
    # 此处记录曾经添加过员工的部门
    redis_client.sadd("departments", department)


def finish_task(number, task, finished=True):
    """
    修改用户任务完成状态
    :param number: 用户ID
    :param task: 任务
    :param finished: 此任务是否完成
    :return: None
    """
    # 将用户信息写入redis
    keys = redis_client.keys(pattern="{}:*".format(number))
    key = keys[0].decode()
    value = {
        task: 1 if finished else 0
    }
    redis_client.hset(name=key, mapping=value)


def reset_department(number, department):
    """
    修改用户部门
    :param number: 用户ID
    :param department: 部门
    :return: None
    """
    # 将用户信息写入redis
    keys = redis_client.keys(pattern="{}:*".format(number))
    key = keys[0].decode()
    redis_client.rename(key, "{}:{}".format(number, department))

    # 此处记录曾经添加过员工的部门
    redis_client.sadd("departments", department)


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
                # print('get message from kafka', record)
                msg = record.value.decode()
                msg_slices = msg.split('|')
                if msg_slices[0] == "new user":
                    number = msg_slices[1]
                    department = msg_slices[2]
                    add_task_employee(number=number, department=department, task="[用户激活]请修改密码来完成用户激活！")
                elif msg_slices[0] == "update password":
                    number = msg_slices[1]
                    finish_task(number=number, task="[用户激活]请修改密码来完成用户激活！")
                elif msg_slices[0] == "update department":
                    number = msg_slices[1]
                    department = msg_slices[2]
                    reset_department(number=number, department=department)

        time.sleep(1)


if __name__ == "__main__":
    consume_threading = threading.Thread(target=consume_kafka, name="ConsumeThreading")
    consume_threading.start()
    app.run(port=5002)
