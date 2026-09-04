class JobProcessor:
    def __init__(self, db_client, redis_client, generator_service):
        self.db = db_client
        self.redis = redis_client
        self.generator = generator_service

    def process(self, job_id):
        archive_bytes = self.db.get_input_archive(job_id)
        zip_bytes, exceptions, count = self.generator.generate(archive_bytes)

        self.db.save_generation_result(job_id, zip_bytes, exceptions, count)

        if exceptions and (zip_bytes and count > 0):
            status = 'completed'
        elif exceptions:
            status = 'failed'
        else:
            status = 'completed'

        self.db.update_job_status(job_id, status)
        self.redis.set_job_status(job_id, status)
        return status