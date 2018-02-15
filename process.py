# coding=utf-8
import os
import json
import shutil
import docker
import requests
import judgelight
from config import Config, Judge, run_status, checker_status


def update(
    site, runid, result, time_used=0, memory_used=0, status=0,
    input_='', output_='', answer='', message='', end=False
):
    assert site == 'tests' or site == 'result' or site == 'compile'
    if site == 'compile':
        data = {
            "site": site,
            "message": message,
            "time_used": time_used,
            "memory_used": memory_used,
            "status": status,
            "result": result
        }
        requests.post(
            'http://127.0.0.1:{}/{}/'.format(Config.webPort, runid), data=data)
    elif site == 'tests':
        data = {
            "site": site,
            "time_used": time_used,
            "memory_used": memory_used,
            "input": input_,
            "output": output_,
            "answer": answer,
            "result": result,
            "message": message,
            "status": status
        }
        requests.post(
            'http://127.0.0.1:{}/{}/'.format(Config.webPort, runid), data=data)
    elif site == 'result':
        data = {
            "site": site,
            "result": result,
            "message": message,
        }
        if end:
            data['end'] = 'True'
        requests.post(
            'http://127.0.0.1:{}/{}/'.format(Config.webPort, runid), data=data)


def init(data):
    """ 进入 docker 之前的初始化操作 """
    runid = data['runid']
    pid = data['pid']
    language = data['language']
    code = data['code']
    time_limit = data['time_limit']
    memory_limit = data['memory_limit']

    work_dir = os.path.join(Config.workDir, runid)
    work_data_dir = os.path.join(work_dir, 'data')
    in_file = [
        {'file': os.path.join('template', 'models.py'), 'to_dir': work_dir}
    ]

    data_json_file = os.path.join(Config.dataDir, pid, 'judge.json')
    if os.path.exists(data_json_file):  # 判断有无 judge.json 文件
        with open(data_json_file) as fr:
            data_json = json.loads(fr.read())
    else:
        data_json = {}

    if 'data' in data_json.keys():  # 添加数据文件
        for data_file in data_json['data']:
            in_file.append({
                'file': os.path.join(Config.dataDir, pid, data_file["in"]),
                'to_dir': work_data_dir
            })
    else:
        data_json['data'] = []
        data_cnt = 1
        file_list = os.listdir(os.path.join(Config.dataDir, pid))
        while True:
            if 'data{}.in'.format(data_cnt) in file_list:
                data_json['data'].append({
                    'in': 'data{}.in'.format(data_cnt),
                    'out': 'data{}.out'.format(data_cnt),
                    'run': 'run{}.out'.format(data_cnt)
                })
                in_file.append({
                    'file': os.path.join(Config.dataDir, pid, 'data{}.in'.format(data_cnt)),
                    'to_dir': work_data_dir
                })
                data_cnt += 1
            else:
                break

    if 'in_file' in data_json.keys():  # 添加 in_file 文件
        for in_data in data_json['in_file']:
            in_file.append({
                'file': os.path.join(Config.dataDir, pid, in_data),
                'to_dir': work_dir
            })

    if os.path.exists(os.path.join(Config.dataDir, pid, 'judge.py')):  # 判断有无 judge.py
        in_file.append({
            'file': os.path.join(Config.dataDir, pid, 'judge.py'),
            'to_dir': work_dir
        })
    else:  # 如果没有显式指定 judge.py 则使用默认的评测程序
        in_file.append({
            'file': os.path.join('template', 'judge.py'),
            'to_dir': work_dir
        })

    # 添加 checker 文件
    if not 'checker' in data_json.keys():
        data_json['checker'] = Judge.default_checker
        in_file.append({
            'file': data_json['checker']['file'],
            'to_dir': work_dir
        })
    else:
        in_file.append({
            'file': os.path.join(Config.dataDir, pid, data_json['checker']['file']),
            'to_dir': work_dir
        })

    data_json.update({
        'file': Judge.cmd[language]['file'],
        'compile_cmd': Judge.cmd[language]['compile'],
        'run_cmd': Judge.cmd[language]['run'],
        'compile_time_limit': Judge.compile_time_limit,
        'compile_memory_limit': Judge.compile_memory_limit,
        'time_limit': time_limit,
        'memory_limit': memory_limit
    })

    with open(os.path.join(work_dir, 'judge.json'), 'w') as judge_json:  # 写入评测配置
        judge_json.write(json.dumps(data_json))
    # 写入代码
    with open(os.path.join(work_dir, Judge.cmd[language]['file']), 'w') as code_file:
        code_file.write(code)
    for i in in_file:
        shutil.copy(i['file'], i['to_dir'])


def run_in_docker(data):
    runid = data['runid']
    devices = os.path.join(os.path.abspath(Config.workDir), runid)
    volumes = {
        devices: {
            'bind': '/work',
            'mode': 'rw'
        }
    }
    client = docker.from_env()
    client.containers.run(
        image=Config.dockerImage,  # docker 的镜像名
        command="python3 judge.py",  # 进入之后执行的操作
        auto_remove=True,  # 运行结束之后自动清理
        cpuset_cpus='1',  # 可使用的 CPU 核数
        network_disabled=True,  # 禁用网络
        network_mode='none',  # 禁用网络
        volumes=volumes,  # 加载数据卷
        working_dir='/work'  # 进入之后的工作目录
    )


def check(data):
    """ 结果评测 """
    runid = data['runid']
    pid = data['pid']
    data_json_file = os.path.join(Config.workDir, runid, 'judge.json')
    work_dir = os.path.join(Config.workDir, runid)
    work_data_dir = os.path.join(work_dir, 'data')
    with open(data_json_file) as data_json:
        data_json = json.loads(data_json.read())
        for data_file in data_json['data']:  # 复制数据文件
            shutil.copy(os.path.join(Config.dataDir, pid,
                                     data_file["out"]), work_data_dir)

    with open(os.path.join(Config.workDir, runid, 'run_out.json')) as fr:
        run_json = json.loads(fr.read())

    # 更新编译状态
    update(site='compile', runid=runid,
           result="pass" if run_json['compile']['pass'] else "nopass",
           time_used=run_json['compile']['time_used'],
           memory_used=run_json['compile']['memory_used'],
           status=run_json['compile']['status'],
           message=run_json['compile']['message'])
    if run_json['compile']['pass'] is False:
        update(site='result', runid=runid, result='Compile Error',
               message=run_json['compile']['message'], end=True)
        return

    abspath = os.path.abspath('./')
    os.chdir(work_dir)  # 修改工作目录
    result = 'Accepted'

    for i in range(len(data_json['data'])):  # 依次评测每组数据
        in_file = os.path.join('data', data_json['data'][i]['in'])
        out_file = os.path.join('data', data_json['data'][i]['out'])
        run_file = os.path.join('data', data_json['data'][i]['run'])

        with open(in_file) as fr:
            input_ = fr.read()[:100]
        with open(run_file) as fr:
            output_ = fr.read()[:100]
        with open(out_file) as fr:
            answer = fr.read()[:100]

        if run_json['run'][i]['status'] != 0:  # 程序运行出错
            this_status = run_status.get(str(run_json['run'][i]['status']), {
                                         'result': 'Runtime Error', 'message': '未知的错误'})
            update(site='tests',
                   runid=runid,
                   result=this_status['result'],
                   input_=input_,
                   output_=output_,
                   answer=answer,
                   message=this_status['message'],
                   time_used=run_json['run'][i]['time_used'],
                   memory_used=run_json['run'][i]['memory_used'],
                   status=run_json['run'][i]['status'])
            if result == 'Accepted':
                result = this_status['result']
            continue

        # 程序运行正常，进行结果评测
        fr = open('checker.out', 'w')
        check = judgelight.JudgeLight()
        check.stderr = fr.fileno()
        check.fork()
        rst = check.run('{} {} {} {}'.format(
            data_json['checker']['cmd'], in_file, run_file, out_file))
        fr.close()
        with open('checker.out') as fr:
            checker_msg = fr.read()[:100]  # 获取 checker 的输出

        this_result = checker_status.get(str(rst.status), 'System Error')
        if this_result == 'System Error':
            checker_msg = '未知的评测输出'

        update(site='tests',
               runid=runid,
               result=this_result,
               input_=input_,
               output_=output_,
               answer=answer,
               message=checker_msg,
               time_used=run_json['run'][i]['time_used'],
               memory_used=run_json['run'][i]['memory_used'],
               status=run_json['run'][i]['status'])
        if result == 'Accepted' and rst.status != 0:
            result = this_result

    os.chdir(abspath)  # 修改回来工作目录
    # 更新最终结果
    update(site='result', runid=runid, result=result, end=True)


def main(data):
    runid = data['runid']
    try:
        init(data)
        update(site='result', runid=runid, result='running')
        run_in_docker(data)
        update(site='result', runid=runid, result='checker')
        check(data)
    except Exception as e:
        print(e)
        update(site='result', runid=runid,
               result='System Error', message=repr(e), end=True)
    else:
        pass
