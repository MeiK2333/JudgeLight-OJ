import time

def judge(token, run_id, problem, language, code, oi=False):
    """ 评测一个提交 """
    # TODO 完成评测逻辑
    print('judge start')
    time.sleep(5)
    print('judge end')
    return {
        'token': token,
        'run_id': 1000,
        'result': 'AC',
        'compilation_info': '',
        'judgement_info': [
            {
                'result': 'AC',
                'time_used': 10,
                'memory_used': 375,
                'signal': 0,
                'syscall': -1,
            }
        ]
    }
