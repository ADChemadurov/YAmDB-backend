![yamdb_workflow](https://github.com/ADChemadurov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# API для YaMDb

## Краткое описание проекта

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Этот конкретный проект является рабочим API для YaMDb.
Вся документация API доступна на /redoc.

В этом проекте используется функционал GitHub Actions. При push'е
кода в репозиторий происходит автоматическое тестирование проекта,
загрузка образа на Docker Hub, деплой на сервере и отправка уведомления
в Telegram (нужно создать бота для этого).

## Запуск проекта

### Установка Docker

Если вы планируете запускать проект на Linux сервере то используйте следующую
команду для установки Docker:
```sudo apt install docker.io```

Так же для использования на Linux сервере нужно установить docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Проверить, что установился docker-compose можно этой командой:
```docker-compose --version```

### Клонирование репозитория на локальную машину

Так же необходимо склонировать репозиторий на свой компьютер.
Для этого необходимо зарегестрироваться на https://github.com/,
а так же установить Git Bash: https://git-scm.com/downloads.
Cделайте fork проекта по этой ссылке в свой репозиторий:
https://github.com/ADChemadurov/infra_sp2
После этого с помощью следующей команды в терминале склонируйте
его на свой компьютер: ```git clone <ваш-username>/<имя-репозитория>```

### Перенос файлов на сервер

Перенесите на сервер следующие файлы:
- Dockerfile;
- docker-compose.yaml
- requirements.txt
А так же папку nginx/.

### Внести значения переменных окружения в GitHub Secrets
Вам не нужно самим создавать файл для переменных окружения.
Для этого настроено автоматическое внесение переменных из GitHub Secrets.
1. Зайдите в репозиторий на GitHub.
2. Нажмите Settings в горизонтальной навигационной панели.
3. Нажмите Secrets в вертикальной навигационной панели.
4. Нажмите New repository secret.
5. В Name вводите имя переменной, в Value значение.

Нужно внести следующие переменные:
1. DOCKER_HUB_USERNAME - имя на Docker Hub
2. DOCKER_HUB_PASSWORD - пароль для Docker Hub
3. HOST_IP_ADDRESS - IP-адрес вашего сервера
4. SERVER_ADMIN_NAME - имя пользователя для сервера
5. SSH_KEY - ssh-ключ
    5.1. получить его можно с помощью команды ```~/.ssh/id_rsa.pub```
6. PASSPHRASE - passphrase для ssh-ключа
7. DB_ENGINE - движок базы данных
8. DB_NAME - имя базы данных
9. POSTGRES_USER - имя администратора базы данных
10. POSTGRES_PASSWORD - пароль
11. DB_HOST - название сервиса (контейнера)
12. DB_PORT - порт для подключения к БД
13. TELEGRAM_CHAT_ID - ID вашего чата в telegram
14. TELEGRAM_TOKEN - токен для вашего бота в telegramm

### Миграции

Так же необходимо произвести все миграции, если их нет в папках
приложений auth_users, categories, reviews.

Для этого запустите следующие 2 команды:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```

Если же нет миграций, а при выполнении двух предыдущих команд
миграции не совершаются, то прозведите миграции отдельно для
каждого приложения:
```
docker-compose exec web python manage.py makemigrations <app_name>
docker-compose exec web python manage.py migrate <app_name> --noinput
```


### Создание суперпользователя

Для доступа в админку нужно создать суперпользователя
с помощью следующей команды:
```
docker-compose exec web python manage.py createsuperuser
```

### Заполнение начальными данными.

Чтобы заполнить базу данных начальными данными используйте
следующие команды команды:
```
sudo docker-compose exec web python3 manage.py shell

# Откроется интерактивная панель:
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit() #  Выход из интерактивной панели.

sudo docker-compose exec web python manage.py loaddata fixtures.json
```


## Технологии

Для запуска проекта вам потребуется:
- Docker
- Git Bash
- Docker Hub
- GitHub Actions
- Telegram
