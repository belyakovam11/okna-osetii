# Окна Осетии

Сайт-каталог окон на Django с калькулятором стоимости и личным кабинетом.

## Запуск локально

Нужен Python 3.9 или новее.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт будет доступен по адресу http://127.0.0.1:8000/, административная панель — `/admin/`.

Для разработки используется небезопасный ключ по умолчанию. При развёртывании задайте `DJANGO_SECRET_KEY` и отключите `DEBUG`.

Локальная база SQLite и пользовательские загрузки из `media/` не входят в репозиторий.
