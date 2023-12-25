import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = PACKAGE_ROOT

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "scaife_viewer.core",
    "scaife_viewer.core.tests",
]
MIDDLEWARE = []
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["scaife_viewer/core/tests/fixtures/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven"t customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
SITE_ID = 1
ROOT_URLCONF = "scaife_viewer.core.tests.urls"
SECRET_KEY = "notasecret"

CTS_API_ENDPOINT = os.environ.get(
    "CTS_API_ENDPOINT", "https://scaife-cts-dev.perseus.org/api/cts"
)
CTS_RESOLVER = {
    "type": "api",
    "kwargs": {"endpoint": CTS_API_ENDPOINT},
}
CTS_LOCAL_TEXT_INVENTORY = "scaife_viewer/core/tests/fixtures/ti.xml"

DEPLOYMENT_TIMESTAMP_VAR_NAME = "foo"
