# coding=utf-8
import json
import redis
import process
from config import Config
from multiprocessing import Pool

rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


def work(runid):
    print('get task ' + runid)
    data = rdc.hget(Config.redisResult, runid)
    process.main(json.loads(bytes.decode(data)))


def main():
    if Config.poolCount > 0:
        pool = Pool(Config.poolCount)
    else:
        pool = Pool()
    while True:
        task = rdc.blpop(Config.redisList)
        runid = bytes.decode(task[1])
        pool.apply_async(work, args=(runid,))
    pool.join()


if __name__ == '__main__':
    main()
