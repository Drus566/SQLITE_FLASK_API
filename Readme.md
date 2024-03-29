# Описание
api.py - программа для управления "задачами" с помощью БД sqlite3 и http сервера Flask.

## Маршруты 
* `/api/get_task/<id>`	[GET] Получить таску
* `/api/get_tasks`	[GET] Получить список тасков
* `/api/task`		[POST] Создать таску `<name> <description> <status>`
* `/api/task<id>`	[PUT] Редактировать таску `<name> <description> <status>`
* `/api/task<id>`	[DELETE] Удалить таску

## Обновления
* Добавил api сервер на свой vps http://90.156.230.242:5000/. Для работы с ним через утилиту `curl` добавил баш скрипты в папку `curl_remote` проекта.

## Сущность "Задача (Task)"
**Поля**:
* id
* name
* description
* status (ADDED, IN_WORK, PERFORMED)

### Примечания
* Оказывается Flask по особенному работает с классами (методы фреймворка без танцев с бубном не поместишь в класс, а также нельзя применять в методах фреймворка своих пользовательские классы)
* Для запросов используется утилита *curl*
* По умолчанию имя БД - 'database.db'

### Скрипты запросов находятся в папке ./curl проекта
* `fill_database` - заполняет базу данных 5 записями
* `create_task <name> <description> <status>` - создает задачу 
* `get_task <id>` - возвращает задачу по id
* `get_tasks` - возвращает список задач
* `update_task <id> <name> <description> <status>` - обновляет задачу с заданным id 
* `delete_task <id>` - удаляет задачу с заданным id

### Пример использования
```shell
n1@tc08:~/python/http_api_sqlite$ python3 api.py

# Запросы будем посылать с помощью curl
n1@tc08:~/python/http_api_sqlite$ cd curl/
n1@tc08:~/python/http_api_sqlite/curl$ ls
create_task  delete_task  fill_database  get_task  get_tasks  update_task
n1@tc08:~/python/http_api_sqlite/curl$ ./fill_database
"success create"
"success create"
"success create"
"success create"
"success create"
n1@tc08:~/python/http_api_sqlite/curl$ ./get_tasks
[[1,"task 1","description of task 1","ADDED"],[2,"task 2","description of task 2","ADDED"],[3,"task 3","description of task 3","ADDED"],[4,"task 4","description of task 4","ADDED"],[5,"task 5","description of task 5","ADDED"]]
n1@tc08:~/python/http_api_sqlite/curl$ ./get_task 3
[[3,"task 3","description of task 3","ADDED"]]
n1@tc08:~/python/http_api_sqlite/curl$ ./update_task 3 'my task' 'my awesome task' PERFORMED
"success update"
n1@tc08:~/python/http_api_sqlite/curl$ ./get_task 3
[[3,"my task","my awesome task","PERFORMED"]]
n1@tc08:~/python/http_api_sqlite/curl$ ./delete_task 3
"success delete"
n1@tc08:~/python/http_api_sqlite/curl$ ./get_task 3
[]
```

### Используемое ПО
* Python: 3.10.12
* SQLite: 3.37.2 
* Flask: 3.0.2
* curl: 7.81.0
