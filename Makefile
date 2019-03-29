help:   ## Show this help message
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'	

all:    ## Build application container and start both app and db
	build up

build:  ## Build application container
	docker-compose build

up:     ## Start both app and db containers in detached mode
	docker-compose up -d

down:   ## Stop both app and db containers
	docker-compose stop

updb:   ## Start only db container in detached mode
	docker-compose up -d db

upapp:  ## Start only app container in detached mode
	docker-compose up -d app

downdb: ## Stop only db container
	docker-compose stop db

downapp:## Stop only app container
	docker-compose stop app
