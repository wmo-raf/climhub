"""
Django settings for climtech project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sys

import dj_database_url
import environ
from climtech.config.telemetry.utils import otel_is_enabled

# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

APP_NAME = env.str("APP_NAME", "climtech")

# Application definition

INSTALLED_APPS = [
    "scout_apm.django",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "taggit",
    "modelcluster",
    "rest_framework",
    "manifest_loader",
    "wagtail",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.users",
    "wagtail.sites",
    "wagtail.images",
    "wagtail.embeds",
    "wagtail.search",
    "wagtail.contrib.redirects",
    "wagtail.contrib.forms",
    "wagtail.api.v2",
    "wagtail.contrib.settings",
    "wagtail.contrib.typed_table_block",
    "wagtail.contrib.search_promotions",
    "climtech.utils",
    "climtech.core",
    "climtech.images",
    "climtech.standardpage",
    "climtech.taxonomy",
    "climtech.search",
    "climtech.navigation",
    "climtech.newsletter",
    "climtech.blog",
    "climtech.features",
    "climtech.packages",
    "climtech.roadmap",
    "climtech.services",
    "climtech.showcase",
    "climtech.sitewide_alert",
    "wagtailmedia",
    "pattern_library",
    "climtech.project_styleguide.apps.ProjectStyleguideConfig",
    "wagtailfontawesomesvg",
    "wagtail_color_panel",
    "wagtailcache",
    "wagtailautocomplete"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

if otel_is_enabled():
    MIDDLEWARE += ["climtech.config.telemetry.middleware.OTELMiddleware"]

ROOT_URLCONF = "climtech.config.urls"
WSGI_APPLICATION = "climtech.config.wsgi.application"
ASGI_APPLICATION = "climtech.config.asgi.application"

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = env.str("STATIC_ROOT", os.path.join(BASE_DIR, "static"))
STATIC_URL = env.str("STATIC_URL", "/static/")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "climtech.core.storage.ManifestStaticFilesStorageNotStrict",
    },
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static_compiled"),)

# Media files
MEDIA_ROOT = env.str("MEDIA_DIR", os.path.join(BASE_DIR, "media"))
MEDIA_URL = env.str("MEDIA_URL", "/media/")

# Basic auth settings
if env.str("BASIC_AUTH_ENABLED", "false").lower() == "true":
    MIDDLEWARE.insert(0, "baipw.middleware.BasicAuthIPWhitelistMiddleware")
    BASIC_AUTH_LOGIN = env.str("BASIC_AUTH_LOGIN", "wagtailorg")
    BASIC_AUTH_PASSWORD = env.str("BASIC_AUTH_PASSWORD", "showmewagtailorg")

    # Wagtail requires Authorization header to be present for the previews
    BASIC_AUTH_DISABLE_CONSUMING_AUTHORIZATION_HEADER = True

    # Paths that shouldn't be protected by basic auth
    if "BASIC_AUTH_WHITELISTED_PATHS" in env:
        BASIC_AUTH_WHITELISTED_PATHS = env.list("BASIC_AUTH_WHITELISTED_PATHS", cast=None, default=[])

    BASIC_AUTH_WHITELISTED_IP_NETWORKS = []

    if "BASIC_AUTH_WHITELISTED_HTTP_HOSTS" in env:
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS = env.list("BASIC_AUTH_WHITELISTED_HTTP_HOSTS", cast=None, default=[])

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DB_ENGINE = 'climtech.config.db_engine'

DATABASES = {
    "default": dj_database_url.config(
        engine=DB_ENGINE,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Template configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_ROOT, "project_styleguide/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "climtech.context_processors.global_pages",
                "climtech.context_processors.theme"
            ],
            "builtins": ["pattern_library.loader_tags"],
        },
    }
]

# Set s-max-age header that is used by reverse proxy/front end cache. See
# urls.py
try:
    CACHE_CONTROL_S_MAXAGE = env.int("CACHE_CONTROL_S_MAXAGE", 600)
except ValueError:
    pass

# Give front-end cache 30 second to revalidate the cache to avoid hitting the
# backend. See urls.py
CACHE_CONTROL_STALE_WHILE_REVALIDATE = env.int("CACHE_CONTROL_STALE_WHILE_REVALIDATE", 30)

SITEWIDE_ALERT_MAXAGE = env.int("SITEWIDE_ALERT_MAXAGE", 300)

SITEWIDE_ALERT_SMAXAGE = env.int("SITEWIDE_ALERT_SMAXAGE", 60 * 60 * 24 * 7)

# Cache
# Use Redis or database as the cache backend
REDIS_TLS_URL = env.str("REDIS_TLS_URL", "")
REDIS_URL = env.str("REDIS_URL", "")

# Prefer the TLS connection URL over non
if REDIS_TLS_URL:
    REDIS_URL = REDIS_TLS_URL

if REDIS_URL:
    connection_pool_kwargs = {}

    if REDIS_URL.startswith("rediss"):
        # Heroku Redis uses self-signed certificates for secure redis conections.
        # https://stackoverflow.com/a/66286068
        # When using TLS, we need to disable certificate validation checks.
        connection_pool_kwargs["ssl_cert_reqs"] = None

    redis_options = {
        "IGNORE_EXCEPTIONS": True,
        "SOCKET_CONNECT_TIMEOUT": 2,  # seconds
        "SOCKET_TIMEOUT": 2,  # seconds
        "CONNECTION_POOL_KWARGS": connection_pool_kwargs,
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"{REDIS_URL}/0",
            "OPTIONS": redis_options,
        },
    }

    DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "database_cache",
        }
    }

# Notification emails
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = env.bool("MODERATION_NOTIFY_SUPERUSERS", False)

# Security configuration
# https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security

# Force HTTPS redirect (enabled by default!)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = False

# This will allow the cache to swallow the fact that the website is behind TLS
# and inform the Django using "X-Forwarded-Proto" HTTP header.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# This is a setting activating the HSTS header. This will enforce the visitors to use
# HTTPS for an amount of time specified in the header. Since we are expecting our apps
# to run via TLS by default, this header is activated by default.
# The header can be deactivated by setting this setting to 0, as it is done in the
# dev and testing settings.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
SECURE_HSTS_SECONDS = DEFAULT_HSTS_SECONDS
if "SECURE_HSTS_SECONDS" in env:
    try:
        SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS")
    except ValueError:
        pass

# Do not use the `includeSubDomains` directive for HSTS. This needs to be prevented
# because the apps are running on client domains (or our own for staging), that are
# being used for other applications as well. We should therefore not impose any
# restrictions on these unrelated applications.
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-content-type-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# Permissions policy settings
# Uses django-permissions-policy to return the header.
# https://github.com/adamchainz/django-permissions-policy
# The list of Chrome-supported features are in:
# https://github.com/w3c/webappsec-permissions-policy/blob/main/features.md
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "picture-in-picture": [],
    "usb": [],
}

# Referrer-policy header settings
# https://django-referrer-policy.readthedocs.io/en/1.0/

REFERRER_POLICY = env.str("SECURE_REFERRER_POLICY", default="no-referrer-when-downgrade")

CLIMTECH_LOG_LEVEL = env.str("CLIMTECH_LOG_LEVEL", "INFO")

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "climtech": {
            "handlers": ["console", "mail_admins"],
            "level": CLIMTECH_LOG_LEVEL,
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console", "mail_admins"],
            "level": CLIMTECH_LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": CLIMTECH_LOG_LEVEL,
    },
}

# Wagtail settings

WAGTAIL_SITE_NAME = "climtech"

WAGTAILIMAGES_IMAGE_MODEL = "images.climtechImage"

WAGTAILIMAGES_EXTENSIONS = ["avif", "jpg", "png", "webp"]

WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    "avif": "avif",
    "webp": "webp",
}

WILLOW_OPTIMIZERS = True

if "PRIMARY_HOST" in env:

    WAGTAILADMIN_BASE_URL = "https://%s" % env.str("PRIMARY_HOST")

# https://docs.wagtail.org/en/v2.8.1/releases/2.8.html#responsive-html-for-embeds-no-longer-added-by-default
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# Search

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Sentry configuration.
is_in_shell = len(sys.argv) > 1 and sys.argv[1] in ["shell", "shell_plus"]

if "SENTRY_DSN" in env and not is_in_shell:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.utils import get_default_release

    sentry_kwargs = {
        "dsn": env.str("SENTRY_DSN"),
        "integrations": [DjangoIntegration()],
    }

    # There's a chooser to toggle between environments at the top right corner on sentry.io
    # Values are typically 'staging' or 'production' but can be set to anything else if needed.
    # heroku config:set SENTRY_ENVIRONMENT=production
    if "SENTRY_ENVIRONMENT" in env:
        sentry_kwargs.update({"environment": env.str("SENTRY_ENVIRONMENT")})

    release = get_default_release()
    if release is None:
        try:
            release = env.str("GIT_REV")
        except KeyError:
            try:
                # Assume this is a Heroku-hosted app with the "runtime-dyno-metadata" lab enabled
                release = env.str("HEROKU_RELEASE_VERSION")
            except KeyError:
                # If there's no commit hash, we do not set a specific release.
                release = None

    sentry_kwargs.update({"release": release})
    sentry_sdk.init(**sentry_kwargs)

# Favicon path
FAVICON_PATH = "img/favicons/favicon.ico"

# Frontend cache

if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env:
    INSTALLED_APPS += ("wagtail.contrib.frontend_cache",)  # noqa
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "EMAIL": env.str("FRONTEND_CACHE_CLOUDFLARE_EMAIL"),
            "TOKEN": env.str("FRONTEND_CACHE_CLOUDFLARE_TOKEN"),
            "ZONEID": env.str("FRONTEND_CACHE_CLOUDFLARE_ZONEID"),
        }
    }

MANIFEST_LOADER = {
    "output_dir": STATICFILES_DIRS[0],
}

PATTERN_LIBRARY_ENABLED = env.bool("PATTERN_LIBRARY_ENABLED", False)

# Pattern library
PATTERN_LIBRARY = {
    # Groups of templates for the pattern library navigation. The keys
    # are the group titles and the values are lists of template name prefixes that will
    # be searched to populate the groups.
    "SECTIONS": (
        ("Style Guide", ["patterns/styleguide"]),
        ("Components", ["patterns/components"]),
        ("Pages", ["patterns/pages"]),
    ),
    # Configure which files to detect as templates.
    "TEMPLATE_SUFFIX": ".html",
    # Set which template components should be rendered inside of,
    # so they may use page-level component dependencies like CSS.
    "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
    # Any template in BASE_TEMPLATE_NAMES or any template that extends a template in
    # BASE_TEMPLATE_NAMES is a "page" and will be rendered as-is without being wrapped.
    "BASE_TEMPLATE_NAMES": ["patterns/base_page.html"],
}

# GitHub integration
GITHUB_ROADMAP_ACCESS_TOKEN = env.str("GITHUB_ROADMAP_ACCESS_TOKEN", "")

# Mailchimp
if "MAILCHIMP_NEWSLETTER_ID" in env and "MAILCHIMP_ACCOUNT_ID" in env:
    MAILCHIMP_ACCOUNT_ID = env.str("MAILCHIMP_ACCOUNT_ID")
    MAILCHIMP_NEWSLETTER_ID = env.str("MAILCHIMP_NEWSLETTER_ID")

# all the tracking
FB_APP_ID = env.str("FB_APP_ID", "")
GOOGLE_TAG_MANAGER_ID = env.str("GOOGLE_TAG_MANAGER_ID", "")
