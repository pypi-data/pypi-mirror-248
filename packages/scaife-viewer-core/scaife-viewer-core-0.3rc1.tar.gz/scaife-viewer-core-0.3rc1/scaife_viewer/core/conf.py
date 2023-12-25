import importlib

from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1 :]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            "Module '{0}' does not define a '{1}'".format(module, attr)
        )
    return attr


class CoreAppConf(AppConf):
    ALLOW_TRAILING_COLON = False

    # Other
    REDIRECT_VERSION_LIBRARY_COLLECTION_TO_READER = True

    HOOKSET = "scaife_viewer.core.hooks.DefaultHookSet"

    # Search Indexing
    USE_CLOUD_INDEXER = False

    # Resolver cache settings
    RESOLVER_CACHE_LABEL = "cts-resolver"

    class Meta:
        prefix = "scaife_viewer_core"

    def configure_hookset(self, value):
        return load_path_attr(value)()
