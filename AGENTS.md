# AGENTS.md — Карта проекта для AI-агентов

Это harness для агентской разработки продуктов. Агент ОБЯЗАН прочитать этот файл перед любой работой.

## Структура
- src/ — исходный код продукта
- tests/ — тесты
- docs/specs/ — спецификации (ЧТО строим)
- docs/plans/ — execution plans (КАК строим)
- docs/rules/ — архитектурные правила
- scripts/ — линтеры
- .claude/ — настройки Claude Code

## Правила
1. Перед задачей: прочитай docs/rules/architecture.md
2. После кода: запусти bash scripts/lint.sh
3. Если линтер ругается — исправь и запусти заново
4. На каждую функцию — тест
5. Не выдумывай зависимости — только то, что в requirements.txt

## Продукт
Простое To-Do приложение на Python + Flask. Детали: docs/specs/product.md

## Запуск
- Установка зависимостей: `pip install -r requirements.txt`
- Запуск приложения: `TODO_SECRET_KEY=<secret> python src/app.py`
  (открывается на http://127.0.0.1:5000)
- Тесты: `pytest`
- Линтер: `bash scripts/lint.sh`
