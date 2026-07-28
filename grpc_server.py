from concurrent import futures

import grpc

from app.handler import generate_from_archive
from proto.generator.generator_pb2 import GenerateResponse
from proto.generator.generator_pb2_grpc import GeneratorServicer, add_GeneratorServicer_to_server


class GeneratorServicer(GeneratorServicer):
    def Generate(self, request, context):
        try:
            result_zip = generate_from_archive(request.archive)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return GenerateResponse()
        return GenerateResponse(
            zip_archive=result_zip,
            errors=[],
            generated_count=0
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GeneratorServicer_to_server(GeneratorServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("Server started in port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()