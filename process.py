# coding=utf-8
from config import Config

import os
import sys
import json
import docker
import shutil
import logging


def set_logging():
    _logger = logging.getLogger("Judger")
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler("judger.log")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)
    # _logger.setLevel(logging.INFO)
    _logger.setLevel(logging.DEBUG)
    return _logger


logger = set_logging()


def env_init(judger):
    run_id = judger.run_id
    pid = judger.pid
    work_dir_path = os.path.join(Config.workDir, run_id)
    problem_data_path = os.path.join(Config.dataDir, pid)

    # Create work dir
    if os.path.exists(work_dir_path):
        shutil.rmtree(work_dir_path)
    os.mkdir(work_dir_path)

    # Copy problem data
    work_data_dir_path = os.path.join(work_dir_path, 'data')
    shutil.copytree(problem_data_path, work_data_dir_path)

    # Writer Judger data to judger.json
    run_data = judger.data
    with open(os.path.join(work_dir_path, 'judger.json'), 'w') as fr:
        fr.write(json.dumps(run_data))

    # Copy config.py
    shutil.copy('config.py', work_dir_path)

    # Copy models.py
    template_path = os.path.join('template')
    shutil.copy(os.path.join(template_path, 'models.py'), work_dir_path)

    # Copy judger.py
    if not os.path.exists(os.path.join(work_dir_path, 'judger.py')):
        shutil.copy(os.path.join(template_path, 'judger.py'), work_dir_path)


def run_in_docker(judger):
    run_id = judger.run_id
    devices = os.path.join(os.path.abspath(Config.workDir), run_id)
    volumes = {
        devices: {
            'bind': '/work',
            'mode': 'rw'
        }
    }
    client = docker.from_env()
    client.containers.run(
        image=Config.dockerImage,  # docker 的镜像名
        command="python3 judger.py",  # 进入之后执行的操作
        auto_remove=True,  # 运行结束之后自动清理
        cpuset_cpus='1',  # 可使用的 CPU 核数
        mem_limit='1024m',  # 可用内存数
        network_disabled=True,  # 禁用网络
        network_mode='none',  # 禁用网络
        volumes=volumes,  # 加载数据卷
        working_dir='/work'  # 进入之后的工作目录
    )


def update_result(judger):
    run_id = judger.run_id
    with open(os.path.join(Config.workDir, run_id, 'result.json')) as fr:
        data = json.loads(fr.read())
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main(judger):
    try:
        logger.info('start judge %s' % judger.run_id)
        env_init(judger)
        logger.info('%s try run docker' % judger.run_id)
        run_in_docker(judger)
        update_result(judger)
    except Exception as er:
        logger.error(repr(er))
    else:
        logger.info('%s judge end' % judger.run_id)
