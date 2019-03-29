# env-request

## Useful commands

### Database Environment Variables
```sh
export DB_HOST=<mysql_host>
export DB_PORT=<mysql_port>
export DB_INSTANCE=<mysql_instance>
export DB_USER=<mysql_user>
export DB_PASSWORD=<mysql_user>
```
### Create database migration after model changes

From inside app folder:

```sh
flask db init #if you want to regenerate migrations folder 
flask db migrate
flask db upgrade
```

### Run the application in development mode

```sh
export FLASK_ENV="development"
export FLASK_APP="main.py"
export FLASK_DEBUG=1

gunicorn -b 0.0.0.0:8000 main:app
```

Server will be exposed at http://127.0.0.1:8000

### Run the application in production mode

```sh
export FLASK_ENV="production"
export FLASK_APP="main.py" 

gunicorn -b 0.0.0.0:8000 main:app
```

Server will be exposed at http://127.0.0.1:8000

## Using Makefile

Makefile is an easy way to build and control the application using Docker and docker-compose.

```sh
$ make help
help:    Show this help message
all:     Build application container and start both app and db
build:   Build application container
up:      Start both app and db containers in detached mode
down:    Stop both app and db containers
updb:    Start only db container in detached mode
upapp:   Start only app container in detached mode
downdb:  Stop only db container
downapp: Stop only app container
```