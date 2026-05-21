"""Общие фикстуры pytest для тестов To-Do приложения."""

import os
import sys

import pytest

_SRC_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"
)
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)


@pytest.fixture
def tasks_file(tmp_path, monkeypatch):
    """Подменить путь к файлу хранилища на временный и вернуть его Path."""
    import storage

    path = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "TASKS_FILE", str(path))
    return path


@pytest.fixture
def client(tasks_file):
    """Flask test client поверх временного хранилища."""
    import app as app_module

    application = app_module.create_app()
    application.config["SECRET_KEY"] = "test-secret"
    application.config["TESTING"] = True
    return application.test_client()
