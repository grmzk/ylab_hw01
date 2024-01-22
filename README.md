# Menus (docker-container)
Docker-контейнер для развертывания проекта Menus (ресурс для управления меню)

##### Технологии
- Python 3.10
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- Pydantic 2.5.3
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

Для работы с другой СУБД отредактировать `.env`

```
POSTGRES_HOST=db            # адрес хоста с БД
POSTGRES_PORT=5432          # порт для подключения к БД
POSTGRES_DB=postgres        # название БД
POSTGRES_USER=postgres      # имя пользователя БД
POSTGRES_PASSWORD=postgres  # пароль пользователя БД
```

Собрать контейнер и запустить Menus:

```
docker-compose up -d
```

Выполнить (только после первой сборки):

```
docker-compose exec application alembic upgrade head
```

##### Эндпоинты

[Полный список эндпоинтов](http://127.0.0.1/api/docs/)

##### Авторы
- Игорь Музыка [mailto:igor@mail.fake]
