import time
import logging
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger("django.request")  # or use a custom logger if preferred

class RequestResponseTrafficLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        start_time = time.time()
        request_start = now()

        # Authenticate user via JWT
        try:
            user_auth_tuple = self.jwt_auth.authenticate(request)
            if user_auth_tuple:
                request.user = user_auth_tuple[0]
        except InvalidToken:
            request.user = AnonymousUser()

        # Call view
        response = self.get_response(request)

        # Calculate duration
        duration = time.time() - start_time
        username = getattr(request.user, "username", "anonymous")

        # Build log entry
        logger.info(
            f"[API LOG] User: {username}, "
            f"Method: {request.method}, "
            f"Path: {request.get_full_path()}, "
            f"Status: {response.status_code}, "
            f"Started at: {request_start.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"Duration: {duration:.2f} sec"
        )

        return response
