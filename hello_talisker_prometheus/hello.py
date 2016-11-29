from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import random
import time

from flask import Flask, redirect
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
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request', ["method", "endpoint"])


def in_progress(**kwargs):
    """Quick hack for SyntaxError on decorator with multiple chained calls."""
    return IN_PROGRESS.labels(**kwargs).track_inprogress()


def request_time(**kwargs):
    """Quick hack for SyntaxError on decorator with multiple chained calls."""
    return REQUEST_TIME.labels(**kwargs).time()


app = Flask(__name__)


@app.route("/")
@in_progress(method='GET', endpoint='/')
@request_time(method='GET', endpoint='/')
def hello():
    REQUESTS.labels(method='GET', endpoint='/').inc()
    # Simulate some work
    time.sleep(random.random())
    return "[{}] Hello World!".format(os.getpid())


@app.route('/metrics')
def metrics():
        return redirect('/_status/metrics')


if __name__ == "__main__":
    app.run()
