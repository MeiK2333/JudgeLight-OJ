import os
import shutil

from JudgeLight import JudgeLight

from config import CONFIG


def judge(token, solution):
    """ 评测一个提交 """
    # TODO 完成评测逻辑
    result = {
        'token': token,
        'run_id': solution['run_id'],
        'result': '',
        'compilation_info': '',
        'judgement_info': []
    }
    work_dir = os.path.join(CONFIG['workdir'], solution['run_id'])
    # 进入评测目录
    os.mkdir(work_dir)
    os.chdir(work_dir)

    # 编译
    compile_info = compile_it(solution)
    result.update(compile_info)

    if compile_info['result'] != 'CE':
        datas = get_all_data(solution)
        # 依次评测每组数据
        for data in datas['data']:
            item_info = judge_one(solution, data, datas['is_spj'])

    # 删除评测目录
    shutil.rmtree(work_dir)
    return result


def judge_one(solution, data, is_spj):
    """ 评测一组数据 """
    time_limit = solution['time_limit']
    memory_limit = solution['memory_limit']
    language = solution['language']

    result = {}

    language_config = CONFIG['language'][language]
    cmd = language_config[language]['run'].split()
    jl = JudgeLight(
        cmd[0], cmd,
        time_limit=time_limit,
        memory_limit=memory_limit,
        real_time_limit=time_limit * 2 + 5000,
        output_size_limit=6553500,
        input_file_path=data['in'],
        output_file_path='output.txt',
        error_file_path='error.txt',
        allow_system_calls_rule='default',
    )
    stats = jl.run()

    return result


def get_all_data(solution):
    """ 获取该题目的所有数据 """
    data_dir = os.path.join(CONFIG['data_folder'], solution['problem_id'])
    files = os.listdir(data_dir)
    datas = {
        'is_spj': True if 'spj.exe' in files else False,
        'data': []
    }
    i = 1
    while True:
        if f'{i}.in' in files and f'{i}.out' in files:
            datas['data'].append({
                'in': os.path.join(data_dir, f'{i}.in'),
                'out': os.path.join(data_dir, f'{i}.out'),
            })
        else:
            break
        i += 1
    return datas


def compile_it(solution):
    """ 编译指定提交 """
    result = {
        'result': '',
        'compilation_info': '',
    }
    language = solution['language']
    code = solution['code']

    language_config = CONFIG['language'][language]

    # 写入代码文件
    with open(language_config['filename'], 'w') as fw:
        fw.write(code)

    cmd = language_config['compile'].split()
    jl = JudgeLight(
        cmd[0], cmd,
        output_file_path='compile_stdout.txt',
        error_file_path='compile_stderr.txt',
        output_size_limit=655350,
        time_limit=5000,
        real_time_limit=10000,
        trace=False,
    )
    stats = jl.run()

    # 判断编译错误
    if stats['signum'] != 0:
        result['result'] = 'CE'
    # 写入编译错误信息
    with open('compile_stderr.txt') as fr:
        result['compilation_info'] = fr.read()
    return result
