import os

import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.getenv('CONFIG_PATH', './config/config.yaml')
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        self.exec_mode = data.get('execution_mode', "")

        self.max_workers = data.get('max_workers', 10)

        grpc_server_cfg = data.get('grpc_server', {})
        self.grpc_server_cfg = {
            'port': int(grpc_server_cfg.get('port', 50051))
        }

        db_cfg = data.get('db', {})
        self.db = {
            'host': db_cfg.get('host', 'localhost'),
            'port': int(db_cfg.get('port', 5432)),
            'db_name': db_cfg.get('db_name', 'generator'),
            'user': db_cfg.get('user'),
            'password': os.getenv('DB_PASSWORD'),
            'max_conn': db_cfg.get('max_conn', 10),
        }

        redis_cfg = data.get('redis', {})
        self.redis = {
            'host': redis_cfg.get('host', 'localhost'),
            'port': int(redis_cfg.get('port', 6379)),
            'password': os.getenv('REDIS_PASSWORD'),
            'job_status_ttl': int(redis_cfg.get('job_status_ttl', 600)),
        }

        rmq_cfg = data.get('rabbit_mq', {})
        self.rabbit_mq = {
            'host': rmq_cfg.get('host', 'localhost'),
            'port': int(rmq_cfg.get('port', 5672)),
            'user': rmq_cfg.get('user'),
            'password': os.getenv('RABBITMQ_PASSWORD'),
            'vhost': rmq_cfg.get('vhost', '/'),
            'queue': rmq_cfg.get('queue', 'jobs')
        }


config = Config()