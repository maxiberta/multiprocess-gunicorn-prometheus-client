WORKERS=4
VENV_PATH = env
BIN = $(VENV_PATH)/bin

all: run

run:
	DEVEL=1 $(BIN)/talisker --access-logfile=- hello_talisker_prometheus.hello:app --bind 0.0.0.0:8000 --reload -w$(WORKERS)

wheels:
	pip wheel -r requirements.txt -w wheels

.PHONY: wheels
