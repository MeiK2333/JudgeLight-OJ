# coding=utf-8
from multiprocessing import Pool

import process
from config import JUDGER_COUNT
from models import get_task, logger


def work(solution):
    if solution is not None:
        logger.info('{} start'.format(solution.runid))
        process.main(solution)
        logger.info('{} end'.format(solution.runid))
    else:
        logger.info('get task failure')


def main():
    if JUDGER_COUNT > 0:
        pool = Pool(JUDGER_COUNT)
    else:
        pool = Pool()

    while True:
        solution = get_task()
        pool.apply_async(work, args=(solution,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
