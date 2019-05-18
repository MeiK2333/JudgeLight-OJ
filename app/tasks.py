from app import celery
from app.judge import judge


@celery.task
def run_judge(token, run_id, problem_id, language, code, oi=True):
    """ 提交 celery 异步执行评测 """
    result = judge(token, run_id, problem_id, language, code, oi)
    return result


@celery.task
def success_callback(result, callback_url):
    """ 评测成功回调（不是 AC，仅代表评测过程没有出现异常错误） """
    # TODO 完成成功回调
    print('success')


@celery.task
def failure_callback(uuid, callback_url):
    """ 评测失败回调（System Error） """
    # TODO 完成失败回调
    print('failure')
