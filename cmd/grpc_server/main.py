from concurrent import futures

import grpc

from internal.app.exceptions import GeneratorError, ErrorCode
from internal.app.generator.handler import generate_from_archive
from internal.config.config import config
from proto.generator.generator_pb2 import GenerateResponse, FileErrors, FileError
from proto.generator.generator_pb2_grpc import GeneratorServicer, add_GeneratorServicer_to_server


class GeneratorServicer(GeneratorServicer):
    def Generate(self, request, context):
        errors = []
        try:
            result_zip, exceptions, cnt = generate_from_archive(request.archive)
            for file_name, file_errors in exceptions.items():
                structered_errors = []
                for err in file_errors:
                    if not isinstance(err, GeneratorError):
                        structered_error = FileError(
                            code=ErrorCode.INTERNAL,
                            message=str(err)
                        )
                    else:
                        structered_error = FileError(
                            code=err.code,
                            message=err.message
                        )
                    structered_errors.append(structered_error)
                errors.append(FileErrors(
                    file_name=file_name,
                    errors=structered_errors
                ))
        except GeneratorError as e:
            context.set_code(e.grpc_code)
            context.set_details(e.message)
            return GenerateResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return GenerateResponse()
        return GenerateResponse(
            zip_archive=result_zip,
            errors=errors,
            generated_count=cnt
        )

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GeneratorServicer_to_server(GeneratorServicer(), server)
    port = config.grpc_server_cfg.get('port')
    server.add_insecure_port(f"[::]:{port}")
    print(f"Server started in port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()