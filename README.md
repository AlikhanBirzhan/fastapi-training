# Finance tracker API

REST API для управления личными финансами с мультивалютной поддержкой. Учебный проект.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **SQLite** — база данных
- **Pydantic v2** — валидация данных
- **Docker** — контейнеризация

## Функционал

- Регистрация пользователей и JWT-авторизация
- Создание кошельков с выбором валюты (USD, EUR, KZT)
- Пополнение и списание средств
- Переводы между кошельками с автоматической конвертацией по курсу
- История операций с фильтрацией по кошельку и датам

## Запуск через Docker

```bash
git clone https://github.com/AlikhanBirzhan/finance-tracker-api
cd fastapi-training-project
docker-compose up --build
```

Открыть документацию: [http://localhost:8000/docs](http://localhost:8000/docs)

## Запуск локально

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
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
| GET | `/api/v1/balance` | Получить баланс кошелька |
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
└── docker-compose.yml
```