"""Точка входа Flask-приложения To-Do."""

import logging
import os

from flask import Flask

import routes
import storage

logger = logging.getLogger(__name__)


def create_app():
    """Создать и сконфигурировать экземпляр Flask-приложения.

    SECRET_KEY (нужен для flash-сообщений) читается из переменной окружения
    TODO_SECRET_KEY и не хранится в коде. При старте выполняется проверка
    хранилища: повреждённый JSON-файл прервёт запуск с явной ошибкой.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("TODO_SECRET_KEY")
    storage.load_tasks()
    app.register_blueprint(routes.bp)
    logger.info("Flask-приложение To-Do сконфигурировано")
    return app


def main():
    """Запустить dev-сервер приложения."""
    logging.basicConfig(level=logging.INFO)
    create_app().run(debug=True)


if __name__ == "__main__":
    main()
