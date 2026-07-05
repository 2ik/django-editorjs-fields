import urllib.parse

from django.conf import settings
from django.utils.module_loading import import_string


def get_default_storage():
    """Get default storage, compatible with Django 4.2–6.x."""
    try:
        from django.core.files.storage import storages  # Django 4.2+
        return storages["default"]
    except ImportError:
        from django.core.files.storage import default_storage
        return default_storage


def get_storage_class():
    storage_path = getattr(
        settings,
        'EDITORJS_STORAGE_BACKEND',
        None,
    )
    if storage_path is not None:
        # Custom storage class from settings
        return import_string(storage_path)()
    return get_default_storage()


def get_hostname_from_url(url):
    obj_url = urllib.parse.urlsplit(url)
    return obj_url.hostname


storage = get_storage_class()
