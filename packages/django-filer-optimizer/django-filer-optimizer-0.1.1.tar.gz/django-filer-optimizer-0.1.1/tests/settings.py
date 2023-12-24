"""Test's settings"""
import os

from django.utils.translation import gettext_noop

DEBUG = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

SECRET_KEY = "NOTASECRET"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "easy_thumbnails",
    "easy_thumbnails.optimize",
    "filer",
    "filer_optimizer",
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [os.path.join(BASE_DIR, "templates")],
    }
]

ROOT_URLCONF = "tests.urls"

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
)

USE_TZ = True
LANGUAGE_CODE = "en"
USE_I18N = True

STATIC_URL = "/static/"

# Languages we provide translations for, out of the box.
LANGUAGES = [
    ("de", gettext_noop("German")),
    ("en", gettext_noop("English")),
    ("es", gettext_noop("Spanish")),
    ("fr", gettext_noop("French")),
    ("it", gettext_noop("Italian")),
    ("ja", gettext_noop("Japanese")),
    ("nl", gettext_noop("Dutch")),
    ("ru", gettext_noop("Russian")),
    ("zh-hans", gettext_noop("Simplified Chinese")),
    ("zh-hant", gettext_noop("Traditional Chinese")),
]

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# THUMBNAIL
THUMBNAIL_PREFIX = "thumbs_"
THUMBNAIL_NAMER = "easy_thumbnails.namers.source_hashed"
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    # 'easy_thumbnails.processors.scale_and_crop',
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)
FILER_STORAGES = {
    "public": {
        "thumbnails": {
            "THUMBNAIL_OPTIONS": {"base_dir": ""},
        },
    },
}
THUMBNAIL_ALIASES = {
    "default": {
        "head": {"size": (1920, 1080), "crop": True},
        "middle": {"size": (1080, 1620), "crop": True},
        "preview": {"size": (750, 480), "crop": True},
        "grid": {"size": (800, 720), "crop": True},
        "70": {"size": (70, 70), "crop": True},
        "130": {"size": (130, 130), "crop": True},
        "250": {"size": (250, 250), "crop": True},
    },
}
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
if os.name != "nt":
    THUMBNAIL_OPTIMIZE_COMMAND = {
        "png": "/usr/bin/optipng {filename}",
        "gif": "/usr/bin/optipng {filename}",
        "jpeg": "/usr/bin/jpegoptim {filename}",
    }

from easy_thumbnails.conf import Settings as thumbnail_settings

THUMBNAIL_PROCESSORS = (
    "image_cropping.thumbnail_processors.crop_corners",
) + thumbnail_settings.THUMBNAIL_PROCESSORS
