### Hexlet tests and linter status:
[![Actions Status](https://github.com/YuliaPie/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/YuliaPie/python-project-52/actions)
### Code Climate Maintainability Badge
[![Maintainability](https://api.codeclimate.com/v1/badges/c9d93e91b19000a87928/maintainability)](https://codeclimate.com/github/YuliaPie/python-project-52/maintainability)
### Link to the domain where the app is deployed:
https://python-project-52-41ik.onrender.com

### About Task Manager

Task Manager – a task management system. It allows setting tasks, assigning performers, and changing their statuses. Registration and authentication are required to work with the system.
The project should be deployed on PaaS. In this case, it is already deployed on render.com. Also, a database is connected to the project. The build command is make install && make migrations, the run command is make start.
SQLite db is used locally, and PostgreSQL is used in production.

To run locally:

Clone the repository locally.

In the command line from the root directory, run the following commands:

- poetry build
- poetry publish --dry-run (you may need to enter your username and password)
- python3 -m pip install --user dist/*.whl
- make start
- follow the link that appears

### О Менеджере задач

Менеджер задач – система управления задачами. Она позволяет ставить задачи, назначать исполнителей и менять их статусы. Для работы с системой требуется регистрация и аутентификация.

Для работы нужно развернуть проект на PaaS. В данном случае он уже развернут на render.com. Также к проекту подсоединена база данных. Команда сборки - make install && make migrations, команда запуска - make start.
Локально используется бд sqlite, а в продакшене — PostgreSQL. 

Для локального запуска:

Склонируйте репозиторий локально.

В командной строке из корневой директории выполните следующие команды:

- poetry build
- poetry publish --dry-run (возможно придется ввести имя пользователя и пароль)
- python3 -m pip install --user dist/*.whl
- make start
- перейти по появившейся ссылке 
