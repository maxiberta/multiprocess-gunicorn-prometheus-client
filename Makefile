WORKERS=4
# Use a fixed shared directory for persistent stats across reboots.
PROMETHEUS_MULTIPROC_DIR=$(shell mktemp -d)

all: run

$(PROMETHEUS_MULTIPROC_DIR):
	mkdir -p $(PROMETHEUS_MULTIPROC_DIR)

run: $(PROMETHEUS_MULTIPROC_DIR)
	DEVEL= prometheus_multiproc_dir=$(PROMETHEUS_MULTIPROC_DIR) talisker --access-logfile=- hello:app --reload -w$(WORKERS)
