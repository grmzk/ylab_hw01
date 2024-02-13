# Menus (docker-container)
Docker-контейнер для развертывания проекта Menus (ресурс для управления меню)

##### Технологии
- Python 3.10
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- Pydantic 2.5.3
- Redis 5.0.1
- PostgreSQL 15
- Nginx 1.24
- Docker

##### Как запустить проект:

Клонировать репозиторий и перейти в директорию `infra` в командной строке:

```
git clone git@github.com:grmzk/ylab_hw01.git
```

```
cd ylab_hw01/infra/
```

Копировать файл `.env.example` в файл `.env`:

```
cp -v .env.example .env
```

При необходимости отредактировать содержимое файла `.env`:

```
COMPOSE_PROJECT_NAME=ylab_hw02

POSTGRES_HOST=db            # адрес хоста с БД
POSTGRES_PORT=5432          # порт для подключения к БД
POSTGRES_DB=postgres        # название БД
POSTGRES_USER=postgres      # имя пользователя БД
POSTGRES_PASSWORD=postgres  # пароль пользователя БД
```

Собрать контейнер и запустить:

```
docker-compose up --build -d
```

Выполнить (только после первой сборки):

```
docker-compose exec app alembic upgrade head
```

##### Эндпоинты

[Полный список эндпоинтов](http://127.0.0.1/api/docs/)

### ТЕСТЫ

Клонировать репозиторий и перейти в директорию `infra_tests` 
в командной строке:

```
git clone git@github.com:grmzk/ylab_hw01.git
```

```
cd ylab_hw01/infra_tests/
```

Копировать файл `.env.example.test` в файл `.env`:

```
cp -v .env.example.test .env
```

При необходимости отредактировать содержимое файла `.env`:

```
COMPOSE_PROJECT_NAME=ylab_hw02_tests

POSTGRES_HOST=db                # адрес хоста с БД
POSTGRES_PORT=5432              # порт для подключения к БД
POSTGRES_DB=postgres_tests      # название БД
POSTGRES_USER=postgres          # имя пользователя БД
POSTGRES_PASSWORD=postgres      # пароль пользователя БД

# Переменные окружения для pytest
POSTGRES_HOST_TEST=db
POSTGRES_PORT_TEST=5432
POSTGRES_DB_TEST=postgres_tests
POSTGRES_USER_TEST=postgres
POSTGRES_PASSWORD_TEST=postgres
```

Собрать контейнер и запустить:

```
docker-compose up --build -d
```

Выполнить:

```
docker-compose exec app pytest -vv
```

##### Авторы
- Игорь Музыка [mailto:igor@mail.fake]
