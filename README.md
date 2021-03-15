# REST API сервис для предложения плейлиста на мероприятии

### Для успешного запуска приложения необходимо проделать следующие действия:

* Клонировать репозиторий с проектом
* Установить зависимости - ```python pip install -r requirements.txt ```
* Создать миграции - ```python python manage.py makemigrations ```
* Применить миграции - ```python python manage.py migrate ```
* Создать суперпользователя для работы с административной частью Django - ```python python manage.py createsuperuser ```
* Запустить сервер - ```python python manage.py runserver ```

---
#### Для приложения установлен ```permissions.IsAuthenticatedOrReadOnly``` перед использованием необходимо получить токен доступа для полноценного использования сервиса

##### Для этого необходимо:

* Зарегистрировать пользователя по маршруту ```/auth/users/``` отправив POST запрос содержащий в теле информацию о пользователе ```{"username": "Ваш никнейм", "password": "Ваш пароль"}```
* Получаем токен доступа по маршруту ```/auth/token/login/``` так же отправив POST запрос содержащий информацию о пользователе
* В ответ получим ответ от сервера ```python {"auth_token": "699a4564646456663f26a656464564c2fb391b05"}```
* Для полноценного использования все запросы должны содержать в себе **Headers**, с авторизацией {"Authorization": "token 699a4564646456663f26a656464564c2fb391b05"}

---

#### Ниже представлены некоторые маршруты приложения, с остальными можно ознакомиться перейдя по пути ```/swagger```

### ```/api/event/```


**GET** - Получить все эвенты

**POST** - Создать эвент, тело запроса ниже

```python
{
    "events": 
        {
            "event_name": "Test Event", # Название эвента
            "start_date": "2021-03-01T21:20:21+03:00", # Дата начала эвента
            "finish_date": "2021-03-31T21:20:24+03:00", # Дата окончания эвента
            "max_tracks": 50 # Лимит на добавление треков в эвент
        }
}
```

### ```/api/event/{Название эвента}/```

**GET** - Получить информацию об выбранном эвенте

**POST** - Аналогично предыдущему POST

**PUT** - Обновить выбранный эвент, отправлять в теле необходимые поля для обновления

**DELETE** - Удалить выбранный эвент


### ```/api/search/{Название трека}/{Название группы**}/page**/{Номер страницы**}/track_id***/{Порядковый номер трека***}/```

**GET** - Получить все/определенный трек(и) с выбранными параметрами для поиска музыки в бесплатном API

**POST** - Добавить выбранный трек в базу данных

`** Необязательные параметры в маршруте`

`*** track_id нужен для получения конкретного трека`


### ```/api/event/{Название эвента}/suggestions/**```

**GET** - Получить предложенные треки для выбранного эвента по убыванию просмотров (треки должны быть в базе данных, добавленны через поиск)

`** В этом маршруте присутствует пагинация, по 5 записей на страницу`

Для добавления трека в плейлист необходимо дополнить маршрут ```../suggestions/{Название трека из предложенных}/```

**GET** - Получить информацию о выбранном треке

**POST** - Добавить трек в выбранный плейлист эвента

`P.S. Трек не добавится в плейлист, если превышен лимит на добавление песен и/или текущая дата не входит в диапозон начала - конца эвента`


### ```/api/music-to-event/{Название эвента}/```

**GET** - Получить список треков, входящих в плейлист (по убыванию просмотров)

**DELETE** - Удалить эвент

**POST** - Добавить трек в выбранный плейлист эвента, тело запроса ниже

```python
{
    "events": 
        {
            "track_name": "Hello? Goodbye!", # Название трека
            "artist": "Lake Street Dive", # Имя исполнителя
            "url": "https://www.last.fm/music/Lake+Street+Dive/_/Hello%3F+Goodbye%21", # Ссылка на трек
            "views": 11866 # Количество прослушиваний/просмотров трека
        }
}
```

`P.S. Трек не добавится в плейлист, если превышен лимит на добавление песен и/или текущая дата не входит в диапозон начала - конца эвента`

