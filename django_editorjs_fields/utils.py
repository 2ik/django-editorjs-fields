import urllib.parse

from django.conf import settings
from django.utils.module_loading import import_string


def get_storage_class():
    return import_string(
        getattr(
            settings,
            'EDITORJS_STORAGE_BACKEND',
            'django.core.files.storage.DefaultStorage',
        )
    )()


def get_hostname_from_url(url):
    obj_url = urllib.parse.urlsplit(url)
    return obj_url.hostname


storage = get_storage_class()
