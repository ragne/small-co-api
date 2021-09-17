from flask import Response, make_response


def make_error(message: str, status: int = 400) -> Response:
    return make_response(({"message": message, "code": status}, status))
