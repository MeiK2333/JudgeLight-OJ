# coding=utf-8
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from config import LANGUAGES
from models import get_result_by_redis, new_solution

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return '''
<form method='post'>
pid: <input name='pid' /><br>
runid: <input name='runid' /><br>
code: <textarea name='code'></textarea><br>
language: <input name='language' /><br>
time_limit: <input name='time_limit'><br>
memory_limit: <input name='memory_limit'></br>
<button type='submit'>Submit</button>
</form>
'''

@app.route('/', methods=['POST'])
def post():
    pid = request.form.get('pid')
    runid = request.form.get('runid')
    code = request.form.get('code')
    language = request.form.get('language')
    time_limit = int(request.form.get('time_limit'))
    memory_limit = int(request.form.get('memory_limit'))
    if language not in LANGUAGES.keys():
        return jsonify({
            'msg': 'language not found',
            'code': -1
        })
    new_solution(pid, runid, code, language, time_limit, memory_limit)
    return jsonify({
        'msg': 'success',
        'code': 0
    })


@app.route('/<runid>/')
def result(runid):
    data = get_result_by_redis(runid)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
