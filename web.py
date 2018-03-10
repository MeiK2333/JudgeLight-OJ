# coding=utf-8
from config import Config
from models import Judger, add_judger_to_list, get_judge_list

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return '''<form method='post'>
run_id: <input name='run_id' required><br>
pid: <input name='pid' required><br>
time_limit: <input name='time_limit' required><br>
memory_limit: <input name='memory_limit' required><br>
language: <input name='language' required><br>
code: <textarea name='code' required></textarea><br>
<button type=submit>submit</button>
</form>'''


@app.route('/', methods=['POST'])
def post():
    """
    Submit a new Judger
    """
    run_id = request.form.get('run_id')

    judger = Judger(run_id)
    data = dict(request.form)
    for i in data:
        data[i] = data[i][0]
    map(lambda x: x[0], data)
    judger.data = data

    judger.update()
    add_judger_to_list(judger)

    return jsonify(request.form)


@app.route('/<int:run_id>/', methods=['GET'])
def get(run_id):
    judger = Judger(run_id)
    return jsonify(judger.data)


@app.route('/<int:run_id>/', methods=['DELETE'])
def delete(run_id):
    judger = Judger(run_id)
    judger.delete()
    return 'Hello World!'


@app.route('/list/')
def judge_list():
    return jsonify(get_judge_list())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=Config.webPort)
