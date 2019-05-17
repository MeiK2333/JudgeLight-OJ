from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

views = Blueprint('views')


@views.route('/', methods=['GET', 'POST'])
async def index(request: Request):
    """
    {
        token,
        problem,
        language,
        code,
    }
    """
    return json('Hello World!')
