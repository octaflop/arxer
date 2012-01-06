#-*- coding: utf-8 -*-
# Django settings for social pinax project.

import os.path
import posixpath
import pinax

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = "verbena"

# informs django of the new verbena user class
AUTH_PROFILE_MODULE = 'verebena.Member'

DEBUG = True
#COMPRESS_ENABLED = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

INTERNAL_IPS = [
    "127.0.0.1",
]

RECAPTCHA_PUBLIC_KEY = "6LcWFsUSAAAAAI9ZJOiTopD96nuIb5I0Rm_ya-yx" # for taskcollab
RECAPTCHA_PRIVATE_KEY = "6LcWFsUSAAAAAHO4s8eGHNcNsqftRXRvbVFf8Zgv" # for taskcollab
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "America/Vancouver"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-ca"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/site_media/static/"

# Local theme for the media files
LOCAL_THEME = "arxer"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "media", LOCAL_THEME),
    os.path.join(PINAX_ROOT, "media", PINAX_THEME),
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = "y2pvlbgq1wc@7v2wd8m2j$)ao*^eh&nolb1u9b$y96vkcj5g^)"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
    ##"django.template.loaders.app_directories.Loader",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "groups.middleware.GroupAwareMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "django_sorting.middleware.SortingMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
##    "django.contrib.sitemaps",
]

ROOT_URLCONF = "arxer.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "staticfiles.context_processors.static_url",
    
    "pinax.core.context_processors.pinax_settings",
    
    "pinax.apps.account.context_processors.account",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
    "messages.context_processors.inbox",
    "friends_app.context_processors.invitations",
    
    "arxer.context_processors.combined_inbox_count",

    #"emencia.django.newsletter.context_processors.media",
]

COMBINED_INBOX_COUNT_SOURCES = [
    "messages.context_processors.inbox",
    "friends_app.context_processors.invitations",
    "notification.context_processors.notification",
]

INSTALLED_APPS = [
    #admin tools
    "filebrowser",
    "admin_tools",
    "admin_tools.theming",
    "admin_tools.menu",
    "admin_tools.dashboard",
   # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.markup",

    # Pinax    
    "pinax.templatetags",
    
    # external
    "notification", # must be first
    "staticfiles",
    "debug_toolbar",
    "mailer",
    "uni_form",
    "django_openid",
    "ajax_validation",
    "timezones",
    "emailconfirmation",
    "announcements",
    "pagination",
    "friends",
    "messages",
    "oembed",
    "groups",
    #"threadedcomments",
    #"wakawaka",
    #"swaps",
    #"voting",
    "tagging",
    #"bookmarks",
    "photologue",
    #"avatar",
    #"flag",
    #"microblogging",
    #"locations",
    "django_sorting",
    #"django_markup",
    "tagging_ext",
    
    # Pinax
    "pinax.apps.account",
    "pinax.apps.signup_codes",
    "pinax.apps.analytics",
    "pinax.apps.profiles",
    #"pinax.apps.blog",
    #"pinax.apps.tribes",
    #"pinax.apps.photos",
    #"pinax.apps.topics",
    #"pinax.apps.threadedcomments_extras",
    #"pinax.apps.voting_extras",

    # Locally installed apps
    "south",
    "django_nose",
    "haystack",
    "tinymce",
    #"emencia.django.newsletter",
    "gencal",

    # project
    "about",

    # ARX
    "verbena",
    "rose", # slideshow app

    "ajax_select",
    "idios",
    "django.contrib.flatpages",
    ##"template_repl",
    "compressor",
    "gunicorn",
    "guardian",
    "easy_maps",
]

# HAYSTACK
HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(PROJECT_ROOT, 'whoosh_index'),
            'INCLUDE_SPELLING': True,
            'BATCH_SIZE': 100,
            }
        }

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

MARKUP_FILTER_FALLBACK = "none"
MARKUP_CHOICES = [
    ("restructuredtext", u"reStructuredText"),
    ("textile", u"Textile"),
    ("markdown", u"Markdown"),
    ("creole", u"Creole"),
]

AUTH_PROFILE_MODULE = "profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

AUTHENTICATION_BACKENDS = [
    "pinax.apps.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
]

ANONYMOUS_USER_ID = -1

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "what_next"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

ugettext = lambda s: s
LANGUAGES = [
    ("en", u"English"),
    ("fr", u"French"),
]

# URCHIN_ID = "ua-..."

YAHOO_MAPS_API_KEY = "S1oXzE_V34FP7CDPXxik7jEFPssOJLQ87aGY_bJSInZ_TYACPjaaAHJWe.yRYjKFtnEF.6Y-"


class NullStream(object):
    def write(*args, **kwargs):
        pass
    writeline = write
    writelines = write

RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    "cloak_email_addresses": True,
    "file_insertion_enabled": False,
    "raw_enabled": False,
    "warning_stream": NullStream(),
    "strip_comments": True,
}

# if Django is running behind a proxy, we need to do things like use
# HTTP_X_FORWARDED_FOR instead of REMOTE_ADDR. This setting is used
# to inform apps of this fact
BEHIND_PROXY = False

FORCE_LOWERCASE_TAGS = True

# Uncomment this line after signing up for a Yahoo Maps API key at the
# following URL: https://developer.yahoo.com/wsregapp/
# YAHOO_MAPS_API_KEY = ""

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

##TEST_RUNNER = "djangonose.testrunner"

ASSETS = STATIC_ROOT
##ASSETS_URL = STATIC_URL

AJAX_LOOKUP_CHANNELS = {
    'member': ('verbena.lookups', 'MemberLookup'),
}

ADMIN_TOOLS_MENU = 'arxer.menu.CustomMenu'
INTERNAL_IPS = ('127.0.0.1',)
TINYMCE_DEFAULT_CONFIG = {
        'theme': 'advanced',
        'custom_undo_redo_levels': 10,
    }


#URL_FILEBROWSER_MEDIA = os.path.join('/site_media/static/filebrowser/')
#PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_ROOT, 'filebrowser/')
# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
