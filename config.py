# coding=utf-8


class Config(object):
    dataDir = './data/'  # data directory
    workDir = './work/'  # judge work directory
    redisList = 'judge_list'  # redis judge list
    redisResult = 'judge_result'  # redis result hash
    poolCount = -1  # the number of processes（-1 on behalf of the default）
    dockerImage = 'judgelight:latest'  # docker Image
    redisHost = '127.0.0.1'  # redis host
    redisPort = '6379'  # redis port
    webPort = 5000  # web port
