from flask import Blueprint, jsonify, request

from app.tasks import failure_callback, run_judge, success_callback

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
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
    task = run_judge.apply_async(
        ('', '', '', '', ''),
        link=success_callback.s(),
        link_error=failure_callback.s()
    )
    return jsonify(task.status)
