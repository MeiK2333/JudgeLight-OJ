from celery import Celery
from sanic import Sanic

celery = Celery(
    broker='amqp://localhost',
    backend='amqp://localhost',
)


def create_app():
    app = Sanic(__name__)

    from app.views import views
    app.blueprint(views)

    return app
