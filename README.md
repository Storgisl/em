Основанная на Django платформа для обмена товарами между пользователями.

## Необходимые условия

- Установленные Docker и Docker Compose
- Python 3.12+ (если работает без Docker)

## Быстрый старт с Docker

1. **Создайте файл окружения** .env.  
``` .env
POSTGRES_HOST=db
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password

DJANGO_SECRET_KEY=your_secret_key
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```
2. Запустите Docker compose:
``` Docker 
docker compose up
```
Веб приложение будет доступно на localhost:8000
