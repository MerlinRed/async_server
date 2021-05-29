## Как запустить проект

1. Установить все библиотеки из requirements.txt

   ```pip3 install -r requirements.txt```

2. Добавить начальные данные в БД

   ```python3 create_start_data.py```

3. Запустить сервер

   ```python3 start_server.py```


>База Данных сделана на SQLite3\
>При запуске проекта, создается файл server/database/server_database.db