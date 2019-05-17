from celery import Celery
from sanic import Sanic
from config import CONFIG

celery = Celery(
    broker=CONFIG['celery_broker'],
    backend=CONFIG['celery_backend'],
)


def create_app(config):
    app = Sanic(__name__)
    app.config.update(config)

    celery.config_from_object(app.config)

    from app.views import views
    app.blueprint(views)

    return app
