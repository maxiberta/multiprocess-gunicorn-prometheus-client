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


# A separate registry is used, as the default registry may contain other
# metrics such as those from the Process Collector.
REGISTRY = CollectorRegistry()

JOB_DURATION = Summary(
    'my_batch_job_duration_seconds', 'Duration of my batch job in seconds.',
    registry=REGISTRY)
RESULT = Gauge(
    'my_batch_job_result', 'This is a test', registry=REGISTRY)
LAST_SUCCESS = Gauge(
    'my_batch_job_last_success_unixtime',
    'Last time my batch job succeeded, in unixtime.', registry=REGISTRY)


@JOB_DURATION.time()
def main():
    if len(sys.argv) < 2:
        print("Usage: {} <Prometheus Pushgateway:port>".format(sys.argv[0]))
        return
    # Simulate some work
    time.sleep(random.random())
    # Update metrics
    RESULT.set(random.random())
    # Update success timestamp
    LAST_SUCCESS.set_to_current_time()
    # Push metrics
    push_to_gateway(sys.argv[1], job='my-batch-job', registry=REGISTRY)


if __name__ == '__main__':
    main()
