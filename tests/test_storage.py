"""Тесты слоя хранения (storage.py)."""

import json

import pytest

import storage


def test_load_tasks_missing_file_returns_empty(tasks_file):
    """Нет файла хранилища — load_tasks возвращает пустой список."""
    assert not tasks_file.exists()
    assert storage.load_tasks() == []


def test_load_tasks_valid_file(tasks_file):
    """Валидный JSON-файл читается в список задач."""
    expected = [{"id": 1, "text": "купить хлеб", "done": False}]
    tasks_file.write_text(json.dumps(expected), encoding="utf-8")
    assert storage.load_tasks() == expected


def test_load_tasks_corrupt_json_raises(tasks_file):
    """Повреждённый JSON приводит к StorageError."""
    tasks_file.write_text("{не json", encoding="utf-8")
    with pytest.raises(storage.StorageError):
        storage.load_tasks()


def test_load_tasks_non_list_raises(tasks_file):
    """Валидный, но не-список JSON приводит к StorageError."""
    tasks_file.write_text('{"id": 1}', encoding="utf-8")
    with pytest.raises(storage.StorageError):
        storage.load_tasks()


def test_save_tasks_roundtrip(tasks_file):
    """save_tasks записывает данные, читаемые обратно load_tasks."""
    tasks = [{"id": 1, "text": "тест", "done": True}]
    storage.save_tasks(tasks)
    assert tasks_file.exists()
    assert storage.load_tasks() == tasks
