help:			## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------- #

build:			## Build or rebuild services
	docker-compose -f docker-compose.yaml build $(c)

up:				## Create and start containers
	docker-compose -f docker-compose.yaml up $(c)

start:			## Start services
	docker-compose -f docker-compose.yaml start $(c)

stop:			## Stop services
	docker-compose -f docker-compose.yaml stop $(c)

down:			## Stop and remove containers, networks, images, and volumes
	docker-compose -f docker-compose.yaml down $(c)

# ---------------------------------------------------- #

build_dev:		## Build or rebuild services for development
	docker-compose -f docker-compose.dev.yaml build $(c)

up_dev:			## Create and start containers for development
	docker-compose -f docker-compose.dev.yaml up $(c)

start_dev:		## Start services for development
	docker-compose -f docker-compose.dev.yaml start $(c)

stop_dev:		## Stop services for development
	docker-compose -f docker-compose.dev.yaml stop $(c)

down_dev:		## Stop and remove containers, networks, images, and volumes for development
	docker-compose -f docker-compose.dev.yaml down $(c)

# ---------------------------------------------------- #

migrations:		## Make django migrations
	docker exec -it drf_shop python manage.py makemigrations

migrate:		## Apply django migrations (migrate)
	docker exec -it drf_shop python manage.py migrate
