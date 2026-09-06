from prometheus_client import Counter, Gauge, Histogram


jobs_in_progress = Gauge(
    "generator_worker_jobs_in_progress",
    "Current number of generation jobs being processed by worker",
    ["mode"],
)

job_processing_duration = Histogram(
    "generator_worker_job_processing_duration_seconds",
    "Time spent processing a generation job inside worker",
    ["mode", "result"],
    buckets=(0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 30, 60),
)

jobs_processed_total = Counter(
    "generator_worker_jobs_processed_total",
    "Total number of jobs processed by worker",
    ["mode", "result"],
)

generation_duration = Histogram(
    "generator_worker_generation_duration_seconds",
    "Time spent specifically generating documents",
    ["mode"],
    buckets=(0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 30, 60),
)

queue_wait_duration = Histogram(
    "generator_queue_wait_duration_seconds",
    "Time a job waits before RabbitMQ worker starts processing it",
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 30, 60),
)