import json
import time

from internal.logger.logger import logger
from internal.metrics import queue_wait_duration


class MessageHandler:
    def __init__(self, job_processor):
        self.processor = job_processor

    def __call__(self, ch, method, properties, body):
        job_id = None
        try:
            data = json.loads(body)
            job_id = data.get('job_id')
            if not job_id:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            enqueued_at_unix_ms = data.get("enqueued_at_unix_ms")
            if enqueued_at_unix_ms is not None:
                wait_seconds = (
                                       time.time() * 1000 - enqueued_at_unix_ms
                               ) / 1000

                if wait_seconds >= 0:
                    queue_wait_duration.observe(wait_seconds)


            status = self.processor.process(job_id)
            logger.info(f"Job {job_id} finished with status {status}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
            self._handle_failure(job_id, str(e))
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def _handle_failure(self, job_id, error):
        try:
            self.processor.db.update_job_status(job_id, 'failed')
            self.processor.db.save_fatal_error(job_id, error)
        except Exception as db_err:
            logger.error(f"Failed to save error: {db_err}")
        self.processor.redis.set_job_status(job_id, 'failed')