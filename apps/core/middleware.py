import logging
import time
import uuid


logger = logging.getLogger("djamedica.request")


class RequestLogMiddleware:
    """
    Registra cada request sin guardar body, passwords ni formularios.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.monotonic()
        request.request_id = uuid.uuid4().hex

        response = self.get_response(request)

        duration_ms = round((time.monotonic() - started_at) * 1000, 2)

        user = getattr(request, "user", None)
        username = user.username if user and user.is_authenticated else "anonymous"

        logger.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%s user=%s",
            request.request_id,
            request.method,
            request.path,
            response.status_code,
            duration_ms,
            username,
        )

        response["X-Request-ID"] = request.request_id
        return response
