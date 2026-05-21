"""Слой хранения задач в JSON-файле на диске."""

import json
import logging
import os
import tempfile

logger = logging.getLogger(__name__)

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_FILE = os.environ.get(
    "TODO_TASKS_FILE", os.path.join(_PROJECT_ROOT, "tasks.json")
)


class StorageError(Exception):
    """Ошибка чтения файла хранилища задач."""


def load_tasks():
    """Загрузить список задач из JSON-файла.

    Если файл отсутствует — возвращается пустой список. Если файл содержит
    невалидный JSON или не список — поднимается StorageError, чтобы приложение
    аварийно завершилось и не затёрло данные.
    """
    if not os.path.exists(TASKS_FILE):
        logger.info(
            "Файл хранилища %s не найден — старт с пустого списка", TASKS_FILE
        )
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as error:
        logger.error("Файл хранилища %s повреждён: %s", TASKS_FILE, error)
        raise StorageError(
            f"Повреждён файл хранилища {TASKS_FILE}: {error}"
        ) from error
    if not isinstance(data, list):
        logger.error("Файл хранилища %s содержит не список задач", TASKS_FILE)
        raise StorageError(
            f"Файл хранилища {TASKS_FILE} должен содержать JSON-массив"
        )
    return data


def save_tasks(tasks):
    """Атомарно сохранить список задач в JSON-файл.

    Запись идёт во временный файл в каталоге хранилища, затем он переименовывается
    поверх целевого. Так данные не теряются при сбое в процессе записи.
    """
    directory = os.path.dirname(TASKS_FILE) or "."
    os.makedirs(directory, exist_ok=True)
    descriptor, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(tasks, handle, ensure_ascii=False, indent=2)
        os.replace(temp_path, TASKS_FILE)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise
    logger.info("Сохранено задач: %d -> %s", len(tasks), TASKS_FILE)
