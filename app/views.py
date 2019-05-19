from flask import Blueprint, jsonify, request

from app.tasks import failure_callback, run_judge, success_callback
from config import CONFIG

views = Blueprint('views', __name__)


@views.route('/', methods=['POST'])
def index():
    """
    {
        token,
        run_id,
        problem,
        time_limit,
        memory_limit,
        language,
        code,
        callback_url,
        oi,
    }
    """
    json_data = request.get_json()
    token = json_data['token']
    run_id = json_data['run_id']
    problem_id = json_data['problem_id']
    time_limit = json_data['time_limit']
    memory_limit = json_data['memory_limit']
    language = json_data['language']
    code = json_data['code']
    callback_url = json_data['callback_url']
    oi = True if json_data.get('oi') is None else False

    if token != CONFIG['token']:
        return jsonify({'message': 'token error!'}, 401)

    solution = {
        'token': token,
        'run_id': run_id,
        'problem_id': problem_id,
        'language': language,
        'time_limit': time_limit,
        'memory_limit': memory_limit,
        'code': code,
        'oi': oi,
    }

    run_judge.apply_async(
        (token, solution),
        link=success_callback.s(solution, callback_url),
        link_error=failure_callback.s(solution, callback_url)
    )

    return jsonify('Success')
