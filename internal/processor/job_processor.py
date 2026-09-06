import time

from internal.metrics import (
    generation_duration,
    job_processing_duration,
    jobs_in_progress,
    jobs_processed_total,
)


class JobProcessor:
    def __init__(self, db_client, redis_client, generator_service):
        self.db = db_client
        self.redis = redis_client
        self.generator = generator_service

    def process(self, job_id):
        processing_start = time.monotonic()
        result = "error"

        jobs_in_progress.labels(mode="queue").inc()

        try:
            archive_bytes = self.db.get_input_archive(job_id)

            generation_start = time.monotonic()

            try:
                zip_bytes, exceptions, count = self.generator.generate(
                    archive_bytes
                )
            finally:
                generation_duration.labels(mode="queue").observe(
                    time.monotonic() - generation_start
                )

            self.db.save_generation_result(
                job_id,
                zip_bytes,
                exceptions,
                count,
            )

            if exceptions and (zip_bytes and count > 0):
                status = "completed"
            elif exceptions:
                status = "failed"
            else:
                status = "completed"

            self.db.update_job_status(job_id, status)
            self.redis.set_job_status(job_id, status)

            result = "success"
            return status

        finally:
            jobs_in_progress.labels(mode="queue").dec()

            jobs_processed_total.labels(
                mode="queue",
                result=result,
            ).inc()

            job_processing_duration.labels(
                mode="queue",
                result=result,
            ).observe(
                time.monotonic() - processing_start
            )