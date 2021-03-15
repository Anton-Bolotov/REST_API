# REST_API


pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


# /api/event/
-- отправить GET запрос для получения всех эвентов;
-- отправить POST запрос с телом ниже, для создания эвента:

{
    "events": 
        {
            "event_name": "Test Event", # Название эвента
            "start_date": "2021-03-01T21:20:21+03:00", # Дата начала эвента
            "finish_date": "2021-03-31T21:20:24+03:00", # Дата окончания эвента
            "max_tracks": 50 # Лимит на добавление треков в эвент
        }
}

# /api/event/{Название эвента}/
-- отправить GET запрос для получения информации об эвенте;
-- отправить POST запрос с телом выше, для создания эвента;
-- отправить PUT запрос для обновления нужных полей эвента;
-- отправить DELETE запрос для удаления эвента.
