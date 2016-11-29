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
)


JOB_DURATION = Summary('my_shared_metrics_batch_job_duration_seconds', 'Duration of my batch job in seconds.')


@JOB_DURATION.time()
def main():
    # A separate registry is used, as the default registry may contain other
    # metrics such as those from the Process Collector.
    registry = CollectorRegistry()
    # Simulate some work
    time.sleep(random.random())
    # Some random gauge
    result = Gauge(
        'my_shared_metrics_batch_job_result', 'This is a test', registry=registry)
    result.set(random.random())
    # Batch job success timestamp
    last_success = Gauge(
        'my_shared_metrics_batch_job_last_success_unixtime', 'Last time my batch job succeeded, in unixtime.', registry=registry)
    last_success.set_to_current_time()


if __name__ == '__main__':
    main()
