# coding=utf-8
import os
import json
import time
import redis
import shutil
from config import Config, Judge
from flask import Flask, request, jsonify

app = Flask(__name__)
rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


@app.route('/')
def index():
    return '''<form method='post'>
runid: <input name='runid'><br>
pid: <input name='pid'><br>
time_limit: <input name='time_limit'><br>
memory_limit: <input name='memory_limit'><br>
language: <input name='language'><br>
code: <textarea name='code'></textarea><br>
<button type=submit>submit</button>
</form>'''


@app.route('/', methods=['POST'])
def post():
    """ 提交一个新的评测 """
    runid = request.form.get('runid')
    pid = request.form.get('pid')
    language = request.form.get('language')
    code = request.form.get('code')
    time_limit = request.form.get('time_limit')
    memory_limit = request.form.get('memory_limit')

    if not (runid and pid and language and code and time_limit and memory_limit):  # 判断内容是否全部填写
        return jsonify({'status': 'error', 'message': 'missing data'})
    try:  # 转换数据类型
        time_limit = int(time_limit)
        memory_limit = int(memory_limit)
    except ValueError as e:
        return jsonify({'status': 'error', 'message': repr(e)})
    if language not in Judge.cmd.keys():  # 判断语言是否存在
        return jsonify({'status': 'error', 'message': 'language ' + language + ' not supported'})
    if os.path.exists(os.path.join(Config.workDir, runid)):  # 判断文件夹是否可用
        return jsonify({'status': 'error', 'message': runid + ' already exists'})
    os.mkdir(os.path.join(Config.workDir, runid))  # 创建文件夹
    os.mkdir(os.path.join(Config.workDir, runid, 'data'))  # 创建数据文件夹

    data = {
        "runid": runid,
        "pid": pid,
        "language": language,
        "code": code,
        "time_limit": time_limit,
        "memory_limit": memory_limit,
        "time_used": 0,
        "memory_used": 0,
        "tests": [],
        "result": "Waiting",
        "message": "",
        "end": False
    }

    rdc.hset(Config.redisResult, runid, json.dumps(data))
    rdc.lpush(Config.redisList, runid)
    return jsonify({'status': 'success', 'data': data})


@app.route('/list/')
def show_judge_list():
    """ 查看评测列表 """
    l = rdc.llen(Config.redisList)
    judge_list = rdc.lrange(Config.redisList, 0, l)
    judge_list_data = []
    for i in judge_list:
        judge_list_data.append(bytes.decode(i))
    return jsonify({'status': 'success', 'data': judge_list_data})


@app.route('/results/')
def show_judge_result():
    """ 查看评测状态 """
    result_keys = rdc.hkeys(Config.redisResult)
    result_data = []
    for i in result_keys:
        result_data.append({
            bytes.decode(i): json.loads(bytes.decode(rdc.hget(Config.redisResult, i)))
        })
    return jsonify({'status': 'success', 'data': result_data})


@app.route('/<runid>/')
def show(runid):
    """ 查看指定 runid 的评测状态 """
    data = rdc.hget(Config.redisResult, runid)
    if data:
        return jsonify({'status': 'success', 'data': json.loads(bytes.decode(data))})
    else:
        return jsonify({'message': runid + ' does not exist', 'status': 'error'})


@app.route('/<runid>/', methods=['POST'])
def update(runid):
    """ 更新指定 runid 的评测状态 """
    site = request.form.get('site')
    result = request.form.get('result', None)
    if result is None:
        return jsonify({'status': 'error', 'message': 'missing result'})

    if site == 'compile':
        time_used = request.form.get('time_used', '0')
        memory_used = request.form.get('memory_used', '0')
        status = request.form.get('status', '0')
        message = request.form.get('message', '')
        try:
            time_used = int(time_used)
            memory_used = int(memory_used)
        except ValueError as e:
            return jsonify({'status': 'error', 'message': repr(e)})
        comdata = {
            "time_used": time_used,
            "memory_used": memory_used,
            "status": status,
            "message": message,
            "result": result
        }

        data = rdc.hget(Config.redisResult, runid)
        data = json.loads(bytes.decode(data))
        data['compile'] = comdata
        rdc.hset(Config.redisResult, runid, json.dumps(data))
    elif site == 'tests':
        time_used = request.form.get('time_used', '0')
        memory_used = request.form.get('memory_used', '0')
        input_ = request.form.get('input', '')
        output_ = request.form.get('output', '')
        answer = request.form.get('answer', '')
        message = request.form.get('message', '')
        status = request.form.get('status', '0')
        try:
            time_used = int(time_used)
            memory_used = int(memory_used)
        except ValueError as e:
            return jsonify({'status': 'error', 'message': repr(e)})

        test = {
            "time_used": time_used,
            "memory_used": memory_used,
            "input": input_,
            "output": output_,
            "answer": answer,
            "result": result,
            "message": message,
            'status': status
        }

        data = rdc.hget(Config.redisResult, runid)
        data = json.loads(bytes.decode(data))
        data['tests'].append(test)
        rdc.hset(Config.redisResult, runid, json.dumps(data))
    elif site == 'result':
        message = request.form.get('message', '')
        end = request.form.get('end', None)

        data = rdc.hget(Config.redisResult, runid)
        data = json.loads(bytes.decode(data))
        data['result'] = result
        data['message'] = message

        if end:
            time_used = 0
            memory_used = 0
            for i in data['tests']:
                time_used = time_used if time_used > i['time_used'] else i['time_used']
                memory_used = memory_used if memory_used > i['memory_used'] else i['memory_used']
            data['time_used'] = time_used
            data['memory_used'] = memory_used
            data['end'] = True
        rdc.hset(Config.redisResult, runid, json.dumps(data))
    else:
        return jsonify({'status': 'error', 'message': 'missing site'})
    return jsonify({'status': 'success', 'data': data})


@app.route('/<runid>/pop/', methods=['POST'])
def pop(runid):
    """ 删除一个已经结束的评测状态 """
    data = rdc.hget(Config.redisResult, runid)
    if not data:
        return jsonify({'status': 'error', 'message': runid + ' does not exist'})
    data = json.loads(bytes.decode(data))
    if data['end'] is False:
        return jsonify({'status': 'error', 'message': runid + ' not finished'})

    rdc.hdel(Config.redisResult, runid)
    shutil.rmtree(os.path.join(Config.workDir, runid))
    return jsonify({'status': 'success', 'data': data})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=Config.webPort)
