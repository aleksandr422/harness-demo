"""Тесты HTTP-маршрутов (routes.py) через Flask test client."""

import service


def test_index_returns_page(client):
    """GET / возвращает страницу со списком задач."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Список задач".encode() in response.data


def test_add_valid_creates_task(client):
    """POST /add с валидным текстом добавляет задачу и делает redirect."""
    response = client.post("/add", data={"text": "новая задача"})
    assert response.status_code == 302
    assert len(service.get_tasks()) == 1


def test_add_empty_creates_nothing(client):
    """POST /add с пробельным текстом не создаёт задачу."""
    response = client.post("/add", data={"text": "   "})
    assert response.status_code == 302
    assert service.get_tasks() == []


def test_add_empty_shows_error(client):
    """Ошибка валидации показывается на странице после redirect."""
    response = client.post("/add", data={"text": ""}, follow_redirects=True)
    assert "пуст".encode() in response.data


def test_toggle_route_flips_status(client):
    """POST /toggle/<id> переключает статус задачи."""
    task = service.add_task("отметить")
    response = client.post(f"/toggle/{task['id']}")
    assert response.status_code == 302
    assert service.get_tasks()[0]["done"] is True


def test_delete_route_removes_task(client):
    """POST /delete/<id> удаляет задачу."""
    task = service.add_task("удалить")
    response = client.post(f"/delete/{task['id']}")
    assert response.status_code == 302
    assert service.get_tasks() == []
