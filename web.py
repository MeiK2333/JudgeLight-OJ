# coding=utf-8
from config import Config
from models import Judger, Result, Runner
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'index'


@app.route('/<int:run_id>/', methods=['GET'])
def get(run_id):
    return 'get %d' % run_id


@app.route('/<int:run_id>/', methods=['POST'])
def post(run_id):
    return 'post %d' % run_id


@app.route('/<int:run_id>/', methods=['DELETE'])
def delete(run_id):
    return 'delete %d' % run_id


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=Config.webPort)
