build:
	poetry install

start:
	poetry gunicorn task_manager.wsgi --log-file -