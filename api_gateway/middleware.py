import logging
import time
from microservices.models import RequestLogs

logger = logging.getLogger(__name__)

class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Filter to log all request to url's that start with any of the strings below.
        self.prefixs = [
            '/get-refresh-token',
            '/service'
        ]

    def __call__(self, request):
        _t = time.time() # Calculated execution time.
        body = request.body
        response = self.get_response(request) # Get response from view function.
        _t = int((time.time() - _t)*1000)    

        # If the url does not start with on of the prefixes above, then return response and dont save log.
        if list(filter(request.get_full_path().startswith, self.prefixs)):

            logger.info('Received request: %s %s', request.method, request.get_full_path())
            logger.info('Sent response: %d', response.status_code)
            # Create instance of our model and assign values
            request_log = RequestLogs(
                endpoint=request.get_full_path(),
                response_code=response.status_code,
                method=request.method,
                remote_address=self.get_client_ip(request),
                exec_time=_t,
                body_request=str(body),
                body_response=str(response.content),
            )

            # # Save log in db
            request_log.save()
        return response

    # get clients ip address
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            _ip = x_forwarded_for.split(',')[0]
        else:
            _ip = request.META.get('REMOTE_ADDR')
        return _ip