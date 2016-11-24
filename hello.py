import os

from flask import Flask
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    REGISTRY,
    generate_latest,
    multiprocess,
)


IN_PROGRESS = Gauge("inprogress_requests", "help", ["method", "endpoint"], multiprocess_mode='livesum')
REQUESTS = Counter("total_requests", "help", ["method", "endpoint"])


def in_progress(**kwargs):
    """Quick hack for SyntaxError on decorator with multiple chained calls."""
    return IN_PROGRESS.labels(**kwargs).track_inprogress()


app = Flask(__name__)


# Expose metrics.
@app.route("/metrics")
@in_progress(method='GET', endpoint='/metrics')
#@IN_PROGRESS.labels(method='GET', endpoint='/metrics').track_inprogress()
def metrics():
    REQUESTS.labels(method='GET', endpoint='/metrics').inc()
    if 'prometheus_multiproc_dir' in os.environ:
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
    else:
        registry = REGISTRY
    data = generate_latest(registry)
    return (data, {'content-type': 'text/plain'})


@app.route("/")
@in_progress(method='GET', endpoint='/')
#@IN_PROGRESS.labels(method='GET', endpoint='/').track_inprogress()
def hello():
    REQUESTS.labels(method='GET', endpoint='/').inc()
    return "[{}] Hello World!".format(os.getpid())


if __name__ == "__main__":
    app.run()
