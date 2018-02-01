# coding=utf-8
import os
import sys
import json


def load_judge_json():
    with open('judge.json') as f:
        return json.loads(f.read())


def load_run_json():
    with open('run_out.json') as f:
        return json.loads(f.read())


def all_run_pass(run_json):
    for i in run_json['run']:
        if i['error'] != 0:
            return False
    return True


def get_run_error(run_json):
    time_limit = run_json['time_limit']
    memory_limit = run_json['memory_limit']
    for i in run_json['run']:
        if i['error'] == 0:
            continue
        if i['time_used'] > time_limit:
            return 'Time Limit Exceeded'
        elif i['memory_used'] > memory_limit:
            return 'Memory Limit Exceeded'
        else:
            return 'Runtime Error'


def check_one(out_data, run_data):
    if out_data.rstrip().lower() == run_data.rstrip().lower():  # 忽略末尾空白符
        return 'Accepted'
    return 'Wrong Answer'


result_data = {
    'result': '',
    'compile': {
        'pass': True,
        'msg': ''
    },
    'run': [],
    'check': []
}


def main():
    judge_data = load_judge_json()
    run_data = load_run_json()

    result_data['compile'] = run_data['compile']
    if result_data['compile']['pass'] is False:
        result_data['result'] = 'Compile Error'
        return

    result_data['run'] = run_data['run']
    if all_run_pass(run_data) is False:
        result_data['result'] = get_run_error(run_data)
        return

    for i in range(len(judge_data['data'])):
        with open(os.path.join('data', judge_data['data'][i]['out'])) as f1:
            in_data = f1.read()
        with open(os.path.join('data', judge_data['data'][i]['run'])) as f2:
            run_data = f2.read()
        rst = check_one(in_data, run_data)
        result_data['check'].append(rst)
        if rst != 'Accepted':
            result_data['result'] = rst
            return False
    return True


if __name__ == '__main__':
    work_dir = sys.argv[1]
    os.chdir(work_dir)
    if main():
        result_data['result'] = 'Accepted'
    with open('judge_out.json', 'w') as f:
        f.write(json.dumps(result_data))
