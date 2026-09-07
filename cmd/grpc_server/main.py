from concurrent import futures

import grpc
import time

from prometheus_client import start_http_server

from internal.app.exceptions import GeneratorError, ErrorCode
from internal.app.generator.handler import generate_from_archive
from internal.config.config import config
from proto.generator.generator_pb2 import GenerateResponse, FileErrors, FileError
from proto.generator.generator_pb2_grpc import GeneratorServicer, add_GeneratorServicer_to_server
from internal.metrics import (
    generation_duration,
    job_processing_duration,
    jobs_in_progress,
    jobs_processed_total,
)


class GeneratorServicer(GeneratorServicer):
    def Generate(self, request, context):
        processing_start = time.monotonic()
        result = "error"

        jobs_in_progress.labels(mode="grpc").inc()

        try:
            errors = []

            try:
                generation_start = time.monotonic()

                try:
                    result_zip, exceptions, cnt = generate_from_archive(
                        request.archive
                    )
                finally:
                    generation_duration.labels(mode="grpc").observe(
                        time.monotonic() - generation_start
                    )

                for file_name, file_errors in exceptions.items():
                    structured_errors = []

                    for err in file_errors:
                        if not isinstance(err, GeneratorError):
                            structured_error = FileError(
                                code=ErrorCode.INTERNAL,
                                message=str(err),
                            )
                        else:
                            structured_error = FileError(
                                code=err.code,
                                message=err.message,
                            )

                        structured_errors.append(structured_error)

                    errors.append(
                        FileErrors(
                            file_name=file_name,
                            errors=structured_errors,
                        )
                    )

            except GeneratorError as e:
                context.set_code(e.grpc_code)
                context.set_details(e.message)
                return GenerateResponse()

            except Exception as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return GenerateResponse()

            result = "success"

            return GenerateResponse(
                zip_archive=result_zip,
                errors=errors,
                generated_count=cnt,
            )

        finally:
            jobs_in_progress.labels(mode="grpc").dec()

            jobs_processed_total.labels(
                mode="grpc",
                result=result,
            ).inc()

            job_processing_duration.labels(
                mode="grpc",
                result=result,
            ).observe(
                time.monotonic() - processing_start
            )

def run_server():
    start_http_server(8001)

    max_workers = config.max_workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_GeneratorServicer_to_server(GeneratorServicer(), server)
    port = config.grpc_server_cfg.get('port')
    server.add_insecure_port(f"[::]:{port}")
    print(f"Server started in port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()