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


storage = get_storage_class()
