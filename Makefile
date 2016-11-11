WORKERS=4
PROMETHEUS_MULTIPROC_DIR="/tmp/prom"

all: run

$(PROMETHEUS_MULTIPROC_DIR):
	mkdir -p $(PROMETHEUS_MULTIPROC_DIR)

run: $(PROMETHEUS_MULTIPROC_DIR)
	DEVEL= prometheus_multiproc_dir=$(PROMETHEUS_MULTIPROC_DIR) talisker --access-logfile=- hello:app --reload -w$(WORKERS)
