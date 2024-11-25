from .base import *  # noqa
from .base import env

MANIFEST_LOADER["cache"] = True  # noqa

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env('DEBUG', False)

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

WAGTAIL_ENABLE_UPDATE_CHECK = False

# Use secure cookies for the session and CSRF cookies.
# If these are set to True, the cookies will be marked as “secure”, which means
# browsers may ensure that the cookies are only sent under an HTTPS connection.
# https://docs.djangoproject.com/en/4.1/ref/settings/#session-cookie-secure
# https://docs.djangoproject.com/en/4.1/ref/settings/#csrf-cookie-secure
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

if "CSRF_TRUSTED_ORIGINS" in env:
    CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', cast=None, default=[])

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str('EMAIL_HOST', default="localhost")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", False)
EMAIL_PORT = os.getenv("EMAIL_PORT", "")

try:
    from .local import *  # noqa
except ImportError:
    pass
