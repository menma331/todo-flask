from flasgger import Swagger
from flask import Flask

from config import DATABASE_URL
from .database.database import DBConnection


def create_app(test_config=None, test=False):
    # создание экземпляра приложения
    app = Flask('Todo List')
    swagger = Swagger(app)

    # Если передана тестовая конфигурация, используем ее
    if test_config:
        app.config.update(test_config)
    else:
        # Обычная конфигурация
        app.config['DATABASE_URL'] = DATABASE_URL

    # инициализирует расширения
    app.db_connection = DBConnection(app.config['DATABASE_URL'], test=test)

    # импортируем представления (views)
    with app.app_context():
        from . import views

    return app
