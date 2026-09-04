import grpc


class GeneratorError(Exception):
    def __init__(self, message: str, code: int = 1000, grpc_code: int | grpc.StatusCode = 13):
        self.message = message
        self.code = code
        self.grpc_code = grpc_code
        super().__init__(message)

class ErrorCode:
    # Общие ошибки (1000-1999)
    EXCEL_NOT_FOUND = 1001
    TEMPLATE_NOT_FOUND = 1002
    NO_CONTRACTORS = 1003
    INTERNAL = 1004

    # Ошибки рендеринга (2000-2999)
    RENDER_FAILED = 2001
    IMAGE_NOT_FOUND = 2002

    # Ошибки парсинга (3000-3999)
    INVALID_EXCEL = 3001
    EMPTY_EXCEL = 3002