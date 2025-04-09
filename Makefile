APP = restapi

test :
#	@flake8 . --exclude .venv -v
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up