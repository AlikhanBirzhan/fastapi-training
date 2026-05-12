# Finance Tracker API

REST API для управления личными финансами с мультивалютной поддержкой. Учебный проект.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **PostgreSQL** — база данных
- **Pydantic v2** — валидация данных
- **Docker** — контейнеризация

## Функционал

- Регистрация пользователей и авторизация через токен
- Создание кошельков с выбором валюты (USD, EUR, KZT)
- Пополнение и списание средств
- Переводы между кошельками с автоматической конвертацией по курсу
- История операций с фильтрацией по кошельку и датам
- Асинхронный клиент для получения курсов валют (httpx)

## Запуск через Docker

1. Создать `.env` файл в корне проекта:

```ini
DATABASE_URL=postgresql://postgres:postgres@db:5432/finance_tracker
POSTGRES_DB=finance_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

2. Запустить контейнеры:

```bash
git clone https://github.com/AlikhanBirzhan/finance-tracker-api
cd finance-tracker-api
docker compose up --build
```

3. Открыть документацию: [http://localhost:8000/docs](http://localhost:8000/docs)

## Запуск локально

1. Убедиться, что PostgreSQL запущен локально и создана база данных `finance_tracker`

2. Создать `.env` файл в корне проекта:

```ini
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/finance_tracker
POSTGRES_DB=finance_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

3. Установить зависимости и запустить:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Авторизация

API использует токен-авторизацию. Токен — это логин пользователя, передаётся в заголовке:

```
Authorization: Bearer <login>
```

Пример — сначала создать пользователя, затем использовать его логин как токен:

```bash
# 1. Создать пользователя
curl -X POST http://localhost:8000/api/v1/users \
  -H 'Content-Type: application/json' \
  -d '{"login": "user1"}'

# 2. Использовать логин как токен
curl http://localhost:8000/api/v1/wallets \
  -H 'Authorization: Bearer user1'
```

## API эндпоинты

### Пользователи

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/users` | Создать пользователя |
| GET | `/api/v1/users/me` | Получить текущего пользователя |

### Кошельки

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/balance` | Получить общий баланс |
| GET | `/api/v1/wallets` | Список всех кошельков |
| POST | `/api/v1/wallets` | Создать кошелёк |

### Операции

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/operations/income` | Пополнить кошелёк |
| POST | `/api/v1/operations/expense` | Списать средства |
| POST | `/api/v1/operations/transfer` | Перевод между кошельками |
| GET | `/api/v1/operations` | История операций |

## Структура проекта

```
.
├── app/
│   ├── api/          # Роутеры и эндпоинты
│   ├── repository/   # Работа с БД
│   ├── service/      # Бизнес-логика
│   ├── models.py     # SQLAlchemy модели
│   └── schemas.py    # Pydantic схемы
├── tests/            # Тесты
├── main.py
├── Dockerfile
├── docker-compose.yml
└── .env.example      # Пример переменных окружения
```