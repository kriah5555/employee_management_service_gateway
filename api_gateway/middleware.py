import logging
import time
from microservices.models import RequestLogs
from microservices.utils import get_microservice_url
import requests
from django.http import HttpResponse
import json

logger = logging.getLogger(__name__)


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Filter to log all request to url's that start with any of the strings below.
        self.prefixs = ["/get-refresh-token", "/service"]

    def __call__(self, request):
        _t = time.time()  # Calculated execution time.
        body = request.body
        response = self.get_response(request)  # Get response from view function.
        _t = int((time.time() - _t) * 1000)

        # If the url does not start with on of the prefixes above, then return response and dont save log.
        if list(filter(request.get_full_path().startswith, self.prefixs)):
            logger.info(
                "Received request: %s %s", request.method, request.get_full_path()
            )
            logger.info("Sent response: %d", response.status_code)
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
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            _ip = x_forwarded_for.split(",")[0]
        else:
            _ip = request.META.get("REMOTE_ADDR")
        return _ip


class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_prefixes = ["/service"]
        self.exclude_paths = [
            "/service/identity-manager/login",
            "/service/identity-manager/login/",
            "/service/identity-manager/web-login",
            "/service/identity-manager/web-login/",
            "/service/identity-manager/oauth/token",
            "/service/identity-manager/generate-access-token",
            "/service/identity-manager/logout",
            "/service/identity-manager/logout/",
        ]
        self.access_token = None
        self.uid = None

    def __call__(self, request):
        if self.should_validate_token(request):
            self.access_token = self.extract_access_token(request)

            if not self.access_token:
                return self.invalid_token_response("Authorization details not provided")

            if not self.validate_token():
                return self.invalid_token_response("No access")

            request.META["HTTP_UID"] = str(self.uid)

        return self.get_response(request)

    def should_validate_token(self, request):
        return (
            any(
                request.get_full_path().startswith(prefix)
                for prefix in self.protected_prefixes
            )
            and request.get_full_path() not in self.exclude_paths
        )

    def extract_access_token(self, request):
        return request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")

    def validate_token(self):
        service_base_url = get_microservice_url("identity-manager")
        url = f"{service_base_url}/validate-token"
        response = requests.get(
            url, headers={"Authorization": f"Bearer {self.access_token}"}
        )

        if response.status_code == 200:
            self.uid = response.json().get("uid", "")
        else:
            return False

        return True

    def invalid_token_response(self, message):
        response_data = {
            "success": False,
            "message": [message],
        }
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
            status=403,
        )
