import os
SITE_NAME = "SFPIRG Development"
CONTACT_EMAIL = "test@example.com"

ROOT_PATH = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS = False
CACHE_BACKEND="locmem:///"
STATIC_URL = "/site_media/static/"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "dev.db",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")
MEDIA_URL = "/site_media/media/"
ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, "grappelli/")
