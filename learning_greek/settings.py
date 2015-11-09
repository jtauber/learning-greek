import os
import urlparse


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

SITE_ID = int(os.environ.get("SITE_ID", 1))
DEBUG = SITE_ID == 1
TEMPLATE_DEBUG = DEBUG

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.db.backends.postgresql_psycopg2"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "learning_greek",
        }
    }

ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = int(os.environ.get("SITE_ID", 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "gvt00tqbcsa*azb9io*w#=9rjlscun*j)8fz*h(5k1wu!gmac!"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "account.context_processors.account",
    "pinax_theme_bootstrap.context_processors.theme",
]


MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "learning_greek.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "learning_greek.wsgi.application"

TEMPLATE_DIRS = [
    os.path.join(PACKAGE_ROOT, "templates"),
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    # theme
    "bootstrapform",
    "pinax_theme_bootstrap",

    # external
    "account",
    "eventlog",
    "metron",
    # "biblion",

    "pinax.lms.activities",

    # project
    "learning_greek",
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USE_AUTH_AUTHENTICATE = True

AUTHENTICATION_BACKENDS = [
    "account.auth_backends.UsernameAuthenticationBackend",
]

ACTIVITIES = {
    # "demographic": "learning_greek.activities.surveys.DemographicSurvey",
    # "spoken-languages": "learning_greek.activities.surveys.SpokenLanguagesSurvey",
    # "goals": "learning_greek.activities.surveys.GoalsSurvey",
    # "previous-greek-knowledge": "learning_greek.activities.surveys.PreviousGreekKnowledge",
    # "suggestion-box": "learning_greek.activities.surveys.SuggestionBox",

    # "uppercase": "learning_greek.activities.alphabet.UpperCaseQuiz",
    # "lowercase": "learning_greek.activities.alphabet.LowerCaseQuiz",
    # "letter-familiarity": "learning_greek.activities.alphabet.LetterFamiliarity",
    # "lowercase-alphabet-order": "learning_greek.activities.alphabet.LowerCaseAlphabetOrderQuiz",
    # "uppercase-with-answers": "learning_greek.activities.alphabet.UpperCaseWithAnswersQuiz",
    # "greek-keyboard": "learning_greek.activities.alphabet.GreekKeyboard",
    # "koine-pronunciation": "learning_greek.activities.alphabet.KoinePronunciation",

    # "recessive-verb-accent": "learning_greek.activities.ltrg.RecessiveVerbAccentQuiz",
    # "persistent-accent": "learning_greek.activities.ltrg.PersistentAccentQuiz",
    "decline-article": "learning_greek.activities.ltrg.DeclineArticleQuiz",
    "decline-demonstrative1": "learning_greek.activities.ltrg.DeclineDemonstrative1Quiz",
    "decline-demonstrative2": "learning_greek.activities.ltrg.DeclineDemonstrative2Quiz",
    "decline-noun1a": "learning_greek.activities.ltrg.DeclineNoun1aQuiz",
    "decline-noun1b": "learning_greek.activities.ltrg.DeclineNoun1bQuiz",
    "decline-noun1c": "learning_greek.activities.ltrg.DeclineNoun1cQuiz",
    "decline-noun1d": "learning_greek.activities.ltrg.DeclineNoun1dQuiz",
    "decline-noun1e": "learning_greek.activities.ltrg.DeclineNoun1eQuiz",
    "decline-noun1f": "learning_greek.activities.ltrg.DeclineNoun1fQuiz",
    "decline-noun2a": "learning_greek.activities.ltrg.DeclineNoun2aQuiz",
    "decline-noun2b": "learning_greek.activities.ltrg.DeclineNoun2bQuiz",
    "adjective12-form": "learning_greek.activities.ltrg.DeclineAdjective12Quiz",
    "omega-primary-active-endings": "learning_greek.activities.ltrg.OmegaVerbsPrimaryActiveEndings",
    "omega-primary-middle-passive-endings": "learning_greek.activities.ltrg.OmegaVerbsPrimaryMiddlePassiveEndings",
    "omega-secondary-active-endings": "learning_greek.activities.ltrg.OmegaVerbsSecondaryActiveEndings",
    "omega-secondary-middle-passive-endings": "learning_greek.activities.ltrg.OmegaVerbsSecondaryMiddlePassiveEndings",
    "chapter3-verb-inflection": "learning_greek.activities.ltrg.Chapter3VerbInflection",
    "chapter4-epsilon-verb-inflection": "learning_greek.activities.ltrg.Chapter4EpsilonContractedVerbInflection",
    "chapter4-alpha-verb-inflection": "learning_greek.activities.ltrg.Chapter4AlphaContractedVerbInflection",
    "chapter4-omicron-verb-inflection": "learning_greek.activities.ltrg.Chapter4OmicronContractedVerbInflection",
    "first-aorist-active-endings": "learning_greek.activities.ltrg.FirstAoristActiveEndings",
    "first-aorist-middle-endings": "learning_greek.activities.ltrg.FirstAoristMiddleEndings",
    "first-aorist-passive-endings": "learning_greek.activities.ltrg.FirstAoristPassiveEndings",
}
