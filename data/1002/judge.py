# coding=utf-8
import os
import json
import judgelight

run_data = {
    'compile': {
        'pass': True,
        'msg': ''
    },
    'run': [],
    'time_limit': -1,
    'memory_limit': -1
}


def load_judge_json():
    with open('judge.json') as f:
        judge_json = f.read()
    return json.loads(judge_json)


def compile_it(data):
    compile_cmd = data['compile_cmd']
    compile_time_limit = data['compile_time_limit']
    compile_memory_limit = data['compile_memory_limit']

    compile_judge = judgelight.JudgeLight()
    compile_judge.time_limit = compile_time_limit
    compile_judge.memory_limit = compile_memory_limit

    compile_out_file = open('compile.out', 'w')
    compile_judge.stderr = compile_out_file.fileno()

    compile_judge.fork()
    rst = compile_judge.run(compile_cmd)

    compile_out_file.close()

    if rst.status == 0:
        return True
    return False


def run_one(cmd, in_file, out_file, time_limit, memory_limit):
    run_judge = judgelight.JudgeLight()
    run_judge.time_limit = time_limit
    run_judge.memory_limit = memory_limit

    judge = judgelight.JudgeLight()
    judge.time_limit = time_limit
    judge.memory_limit = memory_limit

    run_judge.stdin = judge.stdout
    judge.stdin = run_judge.stdout

    judge.fork()
    run_judge.fork()
    judge.run('python3 ')
    rst = run_judge.run(cmd)

    return rst


def run_it(data):
    run_data['time_limit'] = data['time_limit']
    run_data['memory_limit'] = data['memory_limit']
    for i in range(len(data['data'])):
        rst = run_one(data['run_cmd'], os.path.join('data', data['data'][i]["in"]),
                      os.path.join('data', data['data'][i]["run"]), data['time_limit'],
                      data['memory_limit'])
        run_data['run'].append({
            'time_used': rst.time_used,
            'memory_used': rst.memory_used,
            'error': rst.error
        })
        if rst.error != 0:
            return


def main():
    data = load_judge_json()

    run_data['compile']['pass'] = compile_it(data)

    with open('compile.out') as f:
        run_data['compile']['msg'] = f.read()

    if run_data['compile']['pass'] is False:
        return

    run_it(data)


def write_run_result():
    with open('run_out.json', 'w') as f:
        f.write(json.dumps(run_data))


if __name__ == '__main__':
    main()
    write_run_result()
