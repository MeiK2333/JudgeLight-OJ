from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from app.tasks import run_judge, success_callback, failure_callback

views = Blueprint('views')


@views.route('/', methods=['POST'])
async def index(request: Request):
    """
    {
        token,
        run_id,
        problem,
        language,
        code,
        oi,
    }
    """
    # TODO 完成参数解析与数据传递
    result = run_judge.apply_async(
        ('', '', '', '', ''),
        link=success_callback.s(),
        link_error=failure_callback.s()
    )
    return json(result.status)
