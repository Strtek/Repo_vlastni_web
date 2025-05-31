from django.utils.deprecation import MiddlewareMixin

class CookieConsentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.COOKIES.get("cookie_consent") in ["full", "technical"]:
            request.csrf_processing_done = False  # CSRF bude aktivní
        else:
            request.csrf_processing_done = True  # Zablokuj CSRF middleware