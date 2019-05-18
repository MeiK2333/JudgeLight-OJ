from celery import Celery
from flask import Flask

from config import CONFIG

celery = Celery(
    broker=CONFIG['celery_broker'],
    backend=CONFIG['celery_backend'],
)


def create_app(config):
    app = Flask(__name__)
    app.config.update(config)

    celery.config_from_object(app.config)

    from app.views import views
    app.register_blueprint(views)

    return app
