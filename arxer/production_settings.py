COMPRESS=True
COMPRESS_VERSION = True
DEBUG = False
CACHE_BACKEND="memcached://127.0.0.1:11211"
EMAIL_SUBJECT_PREFIX = "[SFPIRG]"
SERVER_EMAIL = "sfpirg@example.com"
DEFAULT_FROM_EMAIL = "noreply@example.com"
USE_I18N = True
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

