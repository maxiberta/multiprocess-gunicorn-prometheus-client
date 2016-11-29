from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import random
import time

from flask import Flask
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    REGISTRY,
    Summary,
    generate_latest,
    multiprocess,
)


IN_PROGRESS = Gauge("inprogress_requests", "help", ["method", "endpoint"], multiprocess_mode='livesum')
REQUESTS = Counter("total_requests", "help", ["method", "endpoint"])
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


def in_progress(**kwargs):
    """Quick hack for SyntaxError on decorator with multiple chained calls."""
    return IN_PROGRESS.labels(**kwargs).track_inprogress()


app = Flask(__name__)


@app.route("/")
@in_progress(method='GET', endpoint='/')
@REQUEST_TIME.time()
def hello():
    REQUESTS.labels(method='GET', endpoint='/').inc()
    # Simulate some work
    time.sleep(random.random())

    return "[{}] Hello World!".format(os.getpid())


if __name__ == "__main__":
    app.run()
