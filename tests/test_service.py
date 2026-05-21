"""Тесты сервисного слоя (service.py)."""

import pytest

import service


def test_validate_text_strips_whitespace(tasks_file):
    """validate_text убирает краевые пробелы."""
    assert service.validate_text("  задача  ") == "задача"


def test_validate_text_empty_raises(tasks_file):
    """Пустой (пробельный) текст отклоняется ValueError."""
    with pytest.raises(ValueError):
        service.validate_text("   ")


def test_validate_text_too_long_raises(tasks_file):
    """Текст длиннее 200 символов отклоняется ValueError."""
    with pytest.raises(ValueError):
        service.validate_text("x" * 201)


def test_validate_text_max_length_ok(tasks_file):
    """Текст ровно 200 символов проходит валидацию."""
    text = "x" * 200
    assert service.validate_text(text) == text


def test_add_task_creates_task(tasks_file):
    """add_task создаёт задачу с done=False и id=1 в пустом хранилище."""
    task = service.add_task("первая")
    assert task["text"] == "первая"
    assert task["done"] is False
    assert task["id"] == 1


def test_add_task_unique_ids(tasks_file):
    """Каждой новой задаче присваивается уникальный id."""
    first = service.add_task("одна")
    second = service.add_task("две")
    assert first["id"] != second["id"]


def test_add_task_empty_raises(tasks_file):
    """add_task с пустым текстом поднимает ValueError."""
    with pytest.raises(ValueError):
        service.add_task("")


def test_add_task_too_long_raises(tasks_file):
    """add_task с текстом длиннее 200 символов поднимает ValueError."""
    with pytest.raises(ValueError):
        service.add_task("x" * 201)


def test_get_tasks_returns_added(tasks_file):
    """get_tasks возвращает ранее добавленные задачи."""
    service.add_task("задача")
    assert len(service.get_tasks()) == 1


def test_delete_task_existing(tasks_file):
    """delete_task удаляет существующую задачу и возвращает True."""
    task = service.add_task("удалить меня")
    assert service.delete_task(task["id"]) is True
    assert service.get_tasks() == []


def test_delete_task_missing(tasks_file):
    """delete_task для несуществующего id возвращает False."""
    assert service.delete_task(999) is False


def test_toggle_task_existing(tasks_file):
    """toggle_task переключает флаг done туда и обратно."""
    task = service.add_task("отметить")
    assert service.toggle_task(task["id"]) is True
    assert service.get_tasks()[0]["done"] is True
    service.toggle_task(task["id"])
    assert service.get_tasks()[0]["done"] is False


def test_toggle_task_missing(tasks_file):
    """toggle_task для несуществующего id возвращает False."""
    assert service.toggle_task(999) is False
