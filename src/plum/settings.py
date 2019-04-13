import configparser
import os
from urllib.parse import urlparse

import sys
from django.utils.crypto import get_random_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get('PLUM_DATA_DIR', os.path.join(BASE_DIR, 'data'))
LOG_DIR = os.path.join(DATA_DIR, 'logs')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static.dist')
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o775
FILE_UPLOAD_PERMISSIONS = 0o644

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

config = configparser.RawConfigParser()
if 'PLUM_CONFIG_FILE' in os.environ:
    config.read_file(open(os.environ.get('PLUM_CONFIG_FILE'), encoding='utf-8'))
else:
    config.read(['/etc/plum/plum.cfg', os.path.expanduser('~/.plum.cfg'), 'plum.cfg'], encoding='utf-8')

SECRET_FILE = os.path.join(DATA_DIR, '.secret')
if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, 'r') as f:
        SECRET_KEY = f.read().strip()
else:
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = get_random_string(50, chars)
    with open(SECRET_FILE, 'w') as f:
        os.chmod(SECRET_FILE, 0o600)
        try:
            os.chown(SECRET_FILE, os.getuid(), os.getgid())
        except AttributeError:
            pass  # os.chown is not available on Windows
        f.write(SECRET_KEY)

debug_default = 'runserver' in sys.argv
DEBUG = os.environ.get('PLUM_DEBUG', str(debug_default)) == 'True'

MAIL_FROM = SERVER_EMAIL = DEFAULT_FROM_EMAIL = os.environ.get('PLUM_MAIL_FROM', config.get('mail', 'from', fallback='admin@localhost'))
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = os.environ.get('PLUM_MAIL_HOST', config.get('mail', 'host', fallback='localhost'))
    EMAIL_PORT = int(os.environ.get('PLUM_MAIL_PORT', config.get('mail', 'port', fallback='25')))
    EMAIL_HOST_USER = os.environ.get('PLUM_MAIL_USER', config.get('mail', 'user', fallback=''))
    EMAIL_HOST_PASSWORD = os.environ.get('PLUM_MAIL_PASSWORD', config.get('mail', 'password', fallback=''))
    EMAIL_USE_TLS = os.environ.get('PLUM_MAIL_TLS', 'False') == 'True'
    EMAIL_USE_SSL = os.environ.get('PLUM_MAIL_SSL', 'False') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + os.getenv('PLUM_DB_TYPE', config.get('database', 'backend', fallback='sqlite3')),
        'NAME': os.getenv('PLUM_DB_NAME', config.get('database', 'name', fallback='db.sqlite3')),
        'USER': os.getenv('PLUM_DB_USER', config.get('database', 'user', fallback='')),
        'PASSWORD': os.getenv('PLUM_DB_PASS', config.get('database', 'password', fallback='')),
        'HOST': os.getenv('PLUM_DB_HOST', config.get('database', 'host', fallback='')),
        'PORT': os.getenv('PLUM_DB_PORT', config.get('database', 'port', fallback='')),
        'CONN_MAX_AGE': 0,
    }
}

SITE_URL = os.getenv('PLUM_SITE_URL', config.get('plum', 'url', fallback='http://localhost'))
if SITE_URL == 'http://localhost':
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [urlparse(SITE_URL).netloc]

if os.getenv('PLUM_COOKIE_DOMAIN', ''):
    SESSION_COOKIE_DOMAIN = os.getenv('PLUM_COOKIE_DOMAIN', '')
    CSRF_COOKIE_DOMAIN = os.getenv('PLUM_COOKIE_DOMAIN', '')

SESSION_COOKIE_SECURE = os.getenv('PLUM_HTTPS', 'True' if SITE_URL.startswith('https:') else 'False') == 'True'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.db"

HAS_REDIS = bool(os.getenv('PLUM_REDIS', ''))
if HAS_REDIS:
    CACHES['default'] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('PLUM_REDIS'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
    CACHES['redis_sessions'] = {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('PLUM_REDIS'),
        "TIMEOUT": 3600 * 24 * 30,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
    if os.getenv('PLUM_REDIS_SESSIONS', 'False') == 'True':
        SESSION_ENGINE = "django.contrib.sessions.backends.cache"
        SESSION_CACHE_ALIAS = "redis_sessions"
    else:
        SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'solo',
    'compressor',
    'plum.core',
    'plum.front',
    'django.contrib.admin.apps.SimpleAdminConfig',
]

try:
    import django_extensions  # noqa

    INSTALLED_APPS.append('django_extensions')
except ImportError:
    pass

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

try:
    import debug_toolbar  # noqa

    if DEBUG:
        INSTALLED_APPS.append('debug_toolbar.apps.DebugToolbarConfig')
        MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
except ImportError:
    pass

ROOT_URLCONF = 'plum.urls'

X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSP_DEFAULT_SRC = ("'self'",)

template_loaders = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
if not DEBUG:
    template_loaders = (
        ('django.template.loaders.cached.Loader', template_loaders),
    )

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(DATA_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                "django.template.context_processors.request",
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'plum.front.context.context_processor'
            ],
            'loaders': template_loaders
        },
    },
]

WSGI_APPLICATION = 'plum.wsgi.application'

if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
]

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), 'locale'),
)

SESSION_COOKIE_NAME = 'plum_session'
CSRF_COOKIE_NAME = 'plum_csrftoken'
SESSION_COOKIE_HTTPONLY = True

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}

INTERNAL_IPS = ('127.0.0.1', '::1')

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGE_SIZE': 50,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'
}

loglevel = 'DEBUG' if DEBUG else 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': loglevel,
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'level': loglevel,
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'plum.log'),
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': loglevel,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': loglevel,
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file', 'console'],
            'level': loglevel,
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file', 'console'],
            'level': 'INFO',  # Do not output all the queries
            'propagate': True,
        }
    },
}

FORMAT_MODULE_PATH = [
    'plum.core.formats',
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_ENABLED = COMPRESS_OFFLINE = not debug_default

COMPRESS_CSS_FILTERS = (
    # CssAbsoluteFilter is incredibly slow, especially when dealing with our _flags.scss
    # However, we don't need it if we consequently use the static() function in Sass
    # 'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter',
)

STATICFILES_DIRS = [
    os.path.join(DATA_DIR, 'static')
] if os.path.exists(os.path.join(DATA_DIR, 'static')) else []

STATICFILES_DIRS += [
    os.path.join(BASE_DIR, 'plum/static')
] if os.path.exists(os.path.join(BASE_DIR, 'plum/static')) else []

AUTH_USER_MODEL = 'core.User'

CURRENCY_PLACES = {
    # default is 2
    'BIF': 0,
    'CLP': 0,
    'DJF': 0,
    'GNF': 0,
    'JPY': 0,
    'KMF': 0,
    'KRW': 0,
    'MGA': 0,
    'PYG': 0,
    'RWF': 0,
    'VND': 0,
    'VUV': 0,
    'XAF': 0,
    'XOF': 0,
    'XPF': 0,
}
