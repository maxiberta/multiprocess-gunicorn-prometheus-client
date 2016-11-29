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


JOB_DURATION = Summary(
    'my_shared_metrics_batch_job_duration_seconds',
    'Duration of my batch job in seconds.')
RESULT = Gauge(
    'my_shared_metrics_batch_job_result', 'This is a test',
    multiprocess_mode='max')
LAST_SUCCESS = Gauge(
    'my_shared_metrics_batch_job_last_success_unixtime',
    'Last time my batch job succeeded, in unixtime.',
    multiprocess_mode='max')


@JOB_DURATION.time()
def main():
    # Simulate some work
    time.sleep(random.random())
    # Set metrics
    RESULT.set(random.random())
    LAST_SUCCESS.set_to_current_time()


if __name__ == '__main__':
    main()
