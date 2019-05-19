import requests

from app import celery
from app.judge import judge


@celery.task
def run_judge(token: str, solution):
    """ 提交 celery 异步执行评测 """
    result = judge(token, solution)
    return result


@celery.task
def success_callback(result, solution, callback_url: str):
    """ 评测成功回调（不是 AC，仅代表评测过程没有出现异常错误） """
    resp = requests.post(callback_url, json=result)
    if resp.status_code != 200:
        raise ValueError('success callback error!')


@celery.task
def failure_callback(uuid, solution, callback_url: str):
    """ 评测失败回调（System Error） """
    result = {
        'token': solution['token'],
        'run_id': solution['run_id'],
        'result': 'SE',
        'compilation_info': '',
        'judgement_info': []
    }
    resp = requests.post(callback_url, json=result)
    if resp.status_code != 200:
        raise ValueError('failure callback error!')
