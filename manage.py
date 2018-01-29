# coding=utf-8
import os
import time
import redis
import process
from config import Config
from multiprocessing import Pool

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


def work(run_id):
    data = rdc.hget(Config.redisResult, run_id)
    process.main(data)
    time.sleep(5)


def main():
    if Config.poolCount > 0:
        pool = Pool(Config.poolCount)
    else:
        pool = Pool()
    while True:
        task = rdc.blpop(Config.redisList)
        run_id = bytes.decode(task[1])
        pool.apply_async(work, args=(run_id,))
    pool.join()


if __name__ == '__main__':
    main()
