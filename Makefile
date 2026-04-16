container_name = kumquat-app-1
build:
	docker compose build
up:
	docker compose up
reset-volumes:
	docker compose down --volumes
run: build up
reset: reset-volumes run

app-shell:
	docker exec -it $(container_name) bash
django-shell:
	docker exec -it $(container_name) ./manage.py shell
