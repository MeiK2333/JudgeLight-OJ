# coding=utf-8
from config import Config
from models import Judger

import os
import sys
import json
import docker
import shutil
import logging


def set_logging():
    logger = logging.getLogger("Judger")
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler("judger.log")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    return logger


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


def run_in_docker(judger):
    pass


def main(judger):
    try:
        logger.info('start judge %s' % judger.run_id)
        env_init(judger)
    except Exception as er:
        logger.error(repr(er))
    else:
        pass
