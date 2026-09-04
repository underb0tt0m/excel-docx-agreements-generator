import pika

from internal.logger.logger import logger


class RabbitMQConsumer:
    def __init__(self, config, message_handler):
        self.config = config
        self.message_handler = message_handler  # callback
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(
            self.config.rabbit_mq['user'],
            self.config.rabbit_mq['password']
        )
        parameters = pika.ConnectionParameters(
            host=self.config.rabbit_mq['host'],
            port=self.config.rabbit_mq['port'],
            virtual_host=self.config.rabbit_mq['vhost'],
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config.rabbit_mq['queue'], durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def start_consuming(self):
        self.channel.basic_consume(
            queue=self.config.rabbit_mq['queue'],
            on_message_callback=self.message_handler
        )
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()