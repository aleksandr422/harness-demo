# Tech Debt

Журнал технического долга и улучшений harness.

## Harness improvements
- be2a98e (2026-05-21): улучшен grep в scripts/lint.sh,
  чтобы не триггерить на подстроку print( внутри Blueprint(,
  pprint() и других идентификаторов. Regex с границей слова.
