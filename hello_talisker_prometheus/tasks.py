import random
import os
import time

from celery import Celery
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Summary,
    push_to_gateway,
)


# A separate registry is used, as the default registry may contain other
# metrics such as those from the Process Collector.
REGISTRY = CollectorRegistry()

DURATION = Summary(
    'my_task_duration_seconds', 'Duration of my task in seconds.',
    registry=REGISTRY)
RESULT = Gauge(
    'my_task_result', 'This is a test task', registry=REGISTRY)
LAST_SUCCESS = Gauge(
    'my_task_last_success_unixtime',
    'Last time my task succeeded, in unixtime.', registry=REGISTRY)


app = Celery('tasks', broker=os.environ.get('BROKER_URL','pyamqp://guest@localhost//'))


@app.task
@DURATION.time()
def add(x, y):
    # Simulate some work
    time.sleep(random.random())
    result = x + y
    # Update metrics
    RESULT.set(result)
    # Update success timestamp
    LAST_SUCCESS.set_to_current_time()
    # Crash if envvar not available...
    PROM_PUSHGW_ADDR = os.environ['PROM_PUSHGW_ADDR']
    # Push metrics
    push_to_gateway(PROM_PUSHGW_ADDR, job='my-celery-worker', registry=REGISTRY)


    return result
