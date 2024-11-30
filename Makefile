APP = restapi

test :
	@flake8 . --exclude .venv -v

compose:
	@docker-compose build
	@docker-compose up