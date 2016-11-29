from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import random
import sys
import time

from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Summary,
    push_to_gateway,
)


JOB_DURATION = Summary('my_batch_job_duration_seconds', 'Duration of my batch job in seconds.')


@JOB_DURATION.time()
def main():
    if len(sys.argv) < 2:
        print("Usage: {} <Prometheus Pushgateway:port>".format(sys.argv[0]))
        return
    registry = CollectorRegistry()
    # Simulate some work
    time.sleep(random.random())
    # Some random gauge
    result = Gauge(
        'my_batch_job_result', 'This is a test', registry=registry)
    result.set(random.random())
    # Batch job success timestamp
    last_success = Gauge(
        'my_batch_job_last_success_unixtime', 'Last time my batch job succeeded, in unixtime.', registry=registry)
    last_success.set_to_current_time()
    # Push metrics
    push_to_gateway(
        sys.argv[1], job='my-batch-job', registry=registry)


if __name__ == '__main__':
    main()
