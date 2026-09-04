import redis

class RedisClient:
    def __init__(self, config):
        self.config = config
        self.client = redis.Redis(
            host=config.redis['host'],
            port=config.redis['port'],
            password=config.redis['password'],
            decode_responses=True
        )

    def set_job_status(self, job_id, status, ttl=None):
        ttl = ttl or self.config.redis.get('job_status_ttl', 600)
        self.client.set(f"job:{job_id}", status, ttl)