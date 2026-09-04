from internal.app.generator.service import GeneratorService
from internal.config.config import config
from internal.infrastructure.db import DatabaseClient
from internal.infrastructure.queue import RabbitMQConsumer
from internal.infrastructure.redis import RedisClient
from internal.processor.job_processor import JobProcessor
from internal.processor.message_handler import MessageHandler


def main():
    db = DatabaseClient(config)
    db.connect()

    redis = RedisClient(config)
    generator = GeneratorService()
    processor = JobProcessor(db, redis, generator)
    handler = MessageHandler(processor)

    consumer = RabbitMQConsumer(config, handler)
    consumer.connect()
    consumer.start_consuming()

    db.close()


if __name__ == '__main__':
    main()