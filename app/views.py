from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

from app.tasks import add

views = Blueprint('views')

@views.route('/', methods=['GET', 'POST'])
async def index(request: Request):
    result = add.apply_async((1, 2))
    return json(result.get(timeout=1))
