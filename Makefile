install:
	poetry install
build:
	./build.sh
start:
	poetry run gunicorn task_manager.wsgi --log-file -

lint:
	poetry run flake8

test:
	 poetry run pytest
	 poetry run coverage report

migrations:
	python manage.py makemigrations
	python manage.py migrate
package-install:
	python -m pip install --user dist/*.whl