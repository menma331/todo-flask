1. Создайте проект и перейдите в него
2. В терминале введите следующую команду:
	```
	git clone git@github.com:menma331/todo-flask.git
	```
3.  После этого перейдите в директорию проекта с помощью
	```
	cd todo-flask
	```
4.  Теперь нужно установить зависимости командой
	```
	pip install -r requirements.txt
	```
 5. Создаем БД в терминале mysql. И заполняем файл .env(нужно создать в директории проекта) по примеру `.env.example`
 6. Создаем миграции командой
	```
	alembic revision --autogenerate -m 'initial'
	```
7. Затем применяем миграции к базе командой
	```
	alembic upgrade head
	```
8. Стартуем приложение
	```
	python runner.py
	```
9. Для документации использовался flasgger. Переходим к документации введя адрес `127.0.0.1:5000/apidocs`
