import logging

logger = logging.getLogger(__name__)

def logging_middleware(get_response):
    def middleware(request):
        logger.info('Received request: %s %s', request.method, request.get_full_path())
        response = get_response(request)
        logger.info('Sent response: %d', response.status_code)
        return response
    return middleware
