from cmd.consumer.main import run_consumer
from cmd.grpc_server.main import run_server
from internal.config.config import config


def main():
    if config.exec_mode == "queue":
        run_consumer()
    elif config.exec_mode == "grpc":
        run_server()
    else:
        raise Exception("unknown execution mode")

if __name__ == "__main__":
    main()