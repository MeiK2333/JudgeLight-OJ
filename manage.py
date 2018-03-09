# coding=utf-8
from config import Config

import process

from models import Judger, get_task
from multiprocessing import Pool


def work(run_id):
    judger = Judger(run_id)
    process.main(judger)


def main():
    if Config.poolCount > 0:
        pool = Pool(Config.poolCount)
    else:
        pool = Pool()

    while True:
        run_id = get_task()
        pool.apply_async(work, args=(run_id,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
