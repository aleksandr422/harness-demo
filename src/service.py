"""Сервисный слой: бизнес-логика управления задачами."""

import logging

import storage

logger = logging.getLogger(__name__)

MAX_TEXT_LENGTH = 200


def validate_text(text):
    """Проверить и нормализовать текст задачи.

    Возвращает текст без краевых пробелов. Поднимает ValueError, если текст
    пустой или длиннее MAX_TEXT_LENGTH символов.
    """
    cleaned = (text or "").strip()
    if not cleaned:
        raise ValueError("Текст задачи не может быть пустым")
    if len(cleaned) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Текст задачи длиннее {MAX_TEXT_LENGTH} символов"
        )
    return cleaned


def get_tasks():
    """Вернуть текущий список задач из хранилища."""
    return storage.load_tasks()


def _next_id(tasks):
    """Вычислить уникальный идентификатор для новой задачи."""
    return max((task["id"] for task in tasks), default=0) + 1


def add_task(text):
    """Добавить новую задачу с заданным текстом.

    Текст валидируется через validate_text. Возвращает созданную задачу
    в виде словаря с полями id, text, done.
    """
    cleaned = validate_text(text)
    tasks = storage.load_tasks()
    task = {"id": _next_id(tasks), "text": cleaned, "done": False}
    tasks.append(task)
    storage.save_tasks(tasks)
    logger.info("Добавлена задача id=%d", task["id"])
    return task


def delete_task(task_id):
    """Удалить задачу по идентификатору.

    Возвращает True, если задача найдена и удалена, иначе False.
    """
    tasks = storage.load_tasks()
    remaining = [task for task in tasks if task["id"] != task_id]
    if len(remaining) == len(tasks):
        logger.warning("Задача id=%s не найдена для удаления", task_id)
        return False
    storage.save_tasks(remaining)
    logger.info("Удалена задача id=%s", task_id)
    return True


def toggle_task(task_id):
    """Переключить флаг выполнения задачи по идентификатору.

    Возвращает True, если задача найдена и статус переключён, иначе False.
    """
    tasks = storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            storage.save_tasks(tasks)
            logger.info(
                "Переключён статус задачи id=%s -> done=%s",
                task_id,
                task["done"],
            )
            return True
    logger.warning("Задача id=%s не найдена для переключения", task_id)
    return False
