# coding=utf-8
import os
import json
import time
import redis
import shutil
from config import Config
from flask import Flask, request, jsonify

app = Flask(__name__)
rdp = redis.ConnectionPool(host=Config.redisHost, port=Config.redisPort)
rdc = redis.StrictRedis(connection_pool=rdp)


@app.route('/')
def index():
    return '''<form method='post'>
run_id: <input name='run_id'><br>
pid: <input name='pid'><br>
code: <input name='code'><br>
<button type=submit>submit</button>
</form>'''


@app.route('/', methods=['POST'])
def add():
    run_id = request.form.get('run_id')
    pid = request.form.get('pid')
    code = request.form.get('code')
    data = request.form
    if run_id and pid and code:
        if os.path.exists(os.path.join(Config.workDir, run_id)):
            return jsonify({'status': 'error', 'msg': run_id + ' 文件夹重名'})
        os.mkdir(os.path.join(Config.workDir, run_id))
        rdc.lpush(Config.redisList, run_id)
        result = {
            'args': data,
            'data': [],
            'end': False
        }
        rdc.hset(Config.redisResult, run_id, json.dumps(result))
        return jsonify({'status': 'success', 'data': data})
    else:
        return jsonify({'status': 'error', 'data': '提供参数不足'})


@app.route('/list/')
def show_judge_list():
    l = rdc.llen(Config.redisList)
    judge_list = rdc.lrange(Config.redisList, 0, l)
    judge_list_data = []
    for i in judge_list:
        judge_list_data.append(bytes.decode(i))
    return jsonify({'status': 'success', 'data': judge_list_data})


@app.route('/results/')
def show_judge_result():
    result_keys = rdc.hkeys(Config.redisResult)
    result_data = []
    for i in result_keys:
        result_data.append({bytes.decode(i): json.loads(rdc.hget(Config.redisResult, i))})
    return jsonify({'status': 'success', 'data': result_data})


@app.route('/<run_id>/')
def show(run_id):
    data = rdc.hget(Config.redisResult, run_id)
    if data:
        return jsonify({'status': 'success', 'data': json.loads(data)})
    else:
        return jsonify({'msg': '要查看的 result 不存在', 'status': 'error'})


@app.route('/<run_id>/', methods=['POST'])
def update(run_id):
    msg = request.form.get('msg')
    end = request.form.get('end')
    result = request.form.get('result')
    data = rdc.hget(Config.redisResult, run_id)
    if msg and data:
        data = json.loads(data)
        data['data'].append({
            'time': int(time.time()),
            'msg': msg
        })
        if end:
            data['end'] = True
        if result:
            data['result'] = result
        rdc.hset(Config.redisResult, run_id, json.dumps(data))
        return jsonify({'status': 'success', 'data': data})
    if msg is None:
        return jsonify({'status': 'error', 'msg': '请提供参数'})
    else:
        return jsonify({'status': 'error', 'msg': '要更新的 result 不存在'})


@app.route('/<run_id>/pop/', methods=['POST'])
def pop(run_id):
    data = rdc.hget(Config.redisResult, run_id)
    if data:
        data = json.loads(data)
        if data['end'] is True:
            rdc.hdel(Config.redisResult, run_id)
            shutil.rmtree(os.path.join(Config.workDir, run_id))
            return jsonify({'status': 'success', 'data': data})
        return jsonify({'status': 'error', 'msg': '指定的 result 还未结束'})
    return jsonify({'status': 'error', 'msg': '指定的 result 不存在'})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
