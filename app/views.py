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
        language,
        code,
        callback_url,
        oi,
    }
    """
    # TODO 完成参数解析与数据传递
    json_data = request.get_json()
    token = json_data.get('token')
    run_id = json_data.get('run_id')
    problem_id = json_data.get('problem_id')
    language = json_data.get('language')
    code = json_data.get('code')
    callback_url = json_data.get('callback_url')
    oi = True if json_data.get('oi') is None else False

    if token != CONFIG['token']:
        return jsonify({}, 401)

    task = run_judge.apply_async(
        (token, run_id, problem_id, language, code, oi),
        link=success_callback.s(callback_url),
        link_error=failure_callback.s(callback_url)
    )
    return jsonify(task.status)
