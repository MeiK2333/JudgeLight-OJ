import time


def judge(token, run_id, problem, language, code, oi=False):
    """ 评测一个提交 """
    # TODO 完成评测逻辑
    print('judge start')
    time.sleep(5)
    print('judge end')
    return [
        {
            'result': 'Accepted',
            'time_used': 10,
            'memory_used': 375,
            'signal': 0,
            'syscall': 0,
        },
    ]
