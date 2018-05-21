# coding=utf-8
import json
import os
import time
from shutil import rmtree

import docker

from config import DATA_DIR, UPDATE_TIME, WORK_DIR
from models import Solution, get_cur_state, logger


def env_init(solution):
    """ 创建评测环境 """
    logger.info('{} env_init'.format(solution.runid))
    work_dir = os.path.join(WORK_DIR, solution.runid)
    if os.path.exists(work_dir):
        rmtree(work_dir)
    os.mkdir(work_dir)

    judge_json = solution.judge_json()

    with open(os.path.join(work_dir, 'judge.json'), 'w') as fw:
        fw.write(json.dumps(judge_json, indent=2, ensure_ascii=False))


def run_in_docker(solution):
    """ 在 docker 中进行评测 """
    logger.info('{} run_in_docker'.format(solution.runid))
    client = docker.from_env()
    runid = solution.runid
    pid = solution.pid

    work_dir = os.path.join(WORK_DIR, runid)
    volumes = {}
    volumes[work_dir] = {
        'bind': '/judgelight/work',
        'mode': 'rw'
    }

    data_dir = os.path.join(DATA_DIR, pid)
    volumes[data_dir] = {
        'bind': '/judgelight/data',
        'mode': 'ro'
    }

    con = client.containers.run(
        image='ubuntu',  # docker 镜像
        command="python3 judger.py /judgelight/work/judge.json",  # 进入后进行的操作
        detach=True,  # 后台运行
        remove=True,  # 运行结束后自动清理
        volumes=volumes,  # 加载数据卷
        working_dir='/judgelight',  # 进入之后的工作目录
        cpuset_cpus='1',  # 可使用的 CPU 核数
        mem_limit='1024m',  # 可用内存数
        network_disabled=True,  # 禁用网络
        network_mode='none',  # 禁用网络
    )
    rf = os.open(os.path.join(work_dir, 'fifo.err'), os.O_RDONLY)
    while True:
        # 更新间隔
        time.sleep(UPDATE_TIME)
        con.reload()
        status = con.status
        data = os.read(rf, 1024)
        if data:
            # 更新评测状态
            solution.update(get_cur_state(data.decode()))
        if status == 'removing' or status == 'exited':
            break
    fr = os.open(os.path.join(work_dir, 'fifo.out'), os.O_RDONLY)
    data = os.read(fr, 102400).decode()
    solution.update(None, json.loads(data))


def env_clear(solution):
    """ 清理评测环境 """
    logger.info('{} env_clear'.format(solution.runid))
    runid = solution.runid
    work_dir = os.path.join(WORK_DIR, runid)
    if os.path.exists(work_dir):
        rmtree(work_dir)


def main(solution):
    env_init(solution)
    run_in_docker(solution)
    env_clear(solution)


if __name__ == '__main__':
    judge_data = {
        'pid': 1000,
        'runid': 1000,
        'code': '''
#include <stdio.h>
int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d\\n", a + b);
    return 0;
}''',
        'language': 'gcc',
        'time_limit': 1000,
        'memory_limit': 65535
    }

    pid = str(judge_data['pid'])
    runid = str(judge_data['runid'])
    code = str(judge_data['code'])
    language = str(judge_data['language'])
    time_limit = int(judge_data['time_limit'])
    memory_limit = int(judge_data['memory_limit'])

    solution = Solution(pid=pid, runid=runid, code=code, language=language,
                        time_limit=time_limit, memory_limit=memory_limit)
    main(solution)
