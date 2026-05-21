#!/bin/bash
echo "=== Запуск линтеров ==="

echo "[1/3] Проверка длины файлов..."
find src -name "*.py" -exec wc -l {} \; | awk '$1 > 200 {print "ОШИБКА: файл слишком длинный:", $2; exit 1}'

echo "[2/3] Проверка на print() в src..."
if grep -rn "print(" src/ 2>/dev/null; then
  echo "ОШИБКА: найдены print() в src/. Используй logging."
  exit 1
fi

echo "[3/3] Проверка импортов..."
if grep -rn "from tests" src/ 2>/dev/null; then
  echo "ОШИБКА: src не должен импортировать из tests."
  exit 1
fi

echo "✓ Все проверки пройдены"
