# Expense Tracker

Учёт трат: добавление, категории, статистика по расходу/доходу.

## Команды
- `/add <amount> <category> [desc]`
- `/stats [category]`
- `/list`
- `/clear`

## Запуск
```bash
cp .env.example .env
# вставь свой TELEGRAM_BOT_TOKEN (от BotFather, не в чат/не в гит)
python3 bot.py
```

## Автор
Создан как часть пакета полезных ботов для Кая. Форк/доработка open-source с указанием автора в NOTICE, если применимо.

## Безопасность
Токены только в .env, не коммитятся. Лицензия MIT для этого проекта.
