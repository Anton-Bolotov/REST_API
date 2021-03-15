# REST API сервис для предложения плейлиста на мероприятии.

### Для успешного запуска приложения необходимо проделать следующие действия:

* Клонировать репозиторий с проектом
* Установить зависимости - ```python pip install -r requirements.txt ```
* Создать миграции - ```python python manage.py makemigrations ```
* Применить миграции - ```python python manage.py migrate ```
* Создать суперпользователя для работы с административной частью Django - ```python python manage.py createsuperuser ```
* Запустить сервер - ```python python manage.py runserver ```

#### Ниже представлены некоторые пути приложения, с остальными можно ознакомиться перейдя по пути ```/swagger```

### /api/event/

**GET** - получить все эвенты

**POST** - создать эвент, тело запроса ниже:

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
### /api/event/{Название эвента}/
-- отправить GET запрос для получения информации об эвенте;
-- отправить POST запрос с телом выше, для создания эвента;
-- отправить PUT запрос для обновления нужных полей эвента;
-- отправить DELETE запрос для удаления эвента.
