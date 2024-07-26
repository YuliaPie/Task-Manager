build:
	poetry install

start:
	poetry run gunicorn task_manager.wsgi --log-file -

lint:
	poetry run flake8

test:
	 poetry run pytest