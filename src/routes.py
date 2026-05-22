"""HTTP-маршруты To-Do приложения (Flask Blueprint)."""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

import service

bp = Blueprint("todo", __name__)


@bp.route("/")
def index():
    """Отобразить главную страницу со списком задач."""
    return render_template("index.html", tasks=service.get_tasks())


@bp.route("/add", methods=["POST"])
def add():
    """Добавить задачу из данных формы и вернуться на главную страницу.

    Ошибка валидации текста показывается пользователю flash-сообщением.
    """
    try:
        service.add_task(request.form.get("text", ""))
    except ValueError as error:
        flash(str(error))
    return redirect(url_for("todo.index"))


@bp.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    """Переключить статус выполнения задачи и вернуться на главную страницу."""
    service.toggle_task(task_id)
    return redirect(url_for("todo.index"))


@bp.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    """Удалить задачу и вернуться на главную страницу."""
    service.delete_task(task_id)
    return redirect(url_for("todo.index"))
