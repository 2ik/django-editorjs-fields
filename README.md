# Editor.js for Django

Django plugin for using [Editor.js](https://editorjs.io/)

> This plugin works fine with JSONField in Django >= 3.1

[![Python versions](https://img.shields.io/pypi/pyversions/django-editorjs-fields)](https://pypi.org/project/django-editorjs-fields/)
[![Python versions](https://img.shields.io/pypi/djversions/django-editorjs-fields)](https://pypi.org/project/django-editorjs-fields/)
[![Downloads](https://pepy.tech/badge/django-editorjs-fields/month)](https://pepy.tech/project/django-editorjs-fields/month)

## Installation

```bash
pip install django-editorjs-fields
```

Add `django_editorjs_fields` to `INSTALLED_APPS` in `settings.py` for your project:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_editorjs_fields',
]
```

## Usage

Add code in your model

```python
# models.py
from django.db import models
from django_editorjs_fields import EditorJsJSONField, EditorJsTextField


class Post(models.Model):
    body_default = models.TextField()
    body_editorjs = EditorJsJSONField()  # Django >= 3.1
    body_editorjs_text = EditorJsTextField()  # Django <= 3.0

```

Or add custom Editor.js plugins and configs ([List plugins](https://github.com/editor-js/awesome-editorjs))

**django-editorjs-fields** includes this list of Editor.js plugins by default:

```python
DEFAULT_PLUGINS = [
    '@editorjs/paragraph',
    '@editorjs/image',
    '@editorjs/header',
    '@editorjs/list',
    '@editorjs/checklist',
    '@editorjs/quote',
    '@editorjs/raw',
    '@editorjs/code',
    '@editorjs/inline-code',
    '@editorjs/embed',
    '@editorjs/delimiter',
    '@editorjs/warning',
    '@editorjs/link',
    '@editorjs/marker',
    '@editorjs/table',
]

DEFAULT_CONFIG_PLUGINS = {
    '@editorjs/image': {
        'Image': {
            'class': 'ImageTool',
            'inlineToolbar': True,
            "config": {"endpoints": {"byFile": "/editorjs/image_upload/"}},
        }
    },
    '@editorjs/header': {
        'Header': {
            'class': 'Header',
            'inlineToolbar': True,
            'config': {
                'placeholder': 'Enter a header',
                'levels': [2, 3, 4],
                'defaultLevel': 2,
            },
        }
    },
    '@editorjs/checklist': {'Checklist': {'class': 'Checklist', 'inlineToolbar': True}},
    '@editorjs/list': {'List': {'class': 'List', 'inlineToolbar': True}},
    '@editorjs/quote': {'Quote': {'class': 'Quote', 'inlineToolbar': True}},
    '@editorjs/raw': {'Raw': {'class': 'RawTool'}},
    '@editorjs/code': {'Code': {'class': 'CodeTool'}},
    '@editorjs/inline-code': {'InlineCode': {'class': 'InlineCode'}},
    '@editorjs/embed': {'Embed': {'class': 'Embed'}},
    '@editorjs/delimiter': {'Delimiter': {'class': 'Delimiter'}},
    '@editorjs/warning': {'Warning': {'class': 'Warning', 'inlineToolbar': True}},
    '@editorjs/link': {'LinkTool': {'class': 'LinkTool'}},
    '@editorjs/marker': {'Marker': {'class': 'Marker', 'inlineToolbar': True}},
    '@editorjs/table': {'Table': {'class': 'Table', 'inlineToolbar': True}},
}
```

Example in models.py

```python
# models.py
from django.db import models
from django_editorjs_fields import EditorJsJSONField


class Post(models.Model):
    body_custom = EditorJsJSONField(
        plugins=[
            "@editorjs/image",
            "@editorjs/header",
            "editorjs-github-gist-plugin",
            "@editorjs/code@2.6.0",  # version allowed :)
            "@editorjs/list@latest",
            "@editorjs/inline-code",
            "@editorjs/table",
        ],
        tools={
            "Image": {
                "config": {
                    "endpoints": {
                        # Your custom backend file uploader endpoint
                        "byFile": "/editorjs/image_upload/"
                    }
                }
            }
        },
        null=True,
        blank=True
    )

```

`EditorJsJSONField` accepts all the arguments of `JSONField` class.

`EditorJsTextField` accepts all the arguments of `TextField` class.

Additionally, it includes arguments such as:

| Args            | Description                                                                                       | Default                  |
| --------------- | ------------------------------------------------------------------------------------------------- | ------------------------ |
| `plugins`       | List plugins Editor.js                                                                            | `DEFAULT_PLUGINS`        |
| `tools`         | Set config `tools` for Editor.js [See docs](https://editorjs.io/configuration#passing-saved-data) | `DEFAULT_CONFIG_PLUGINS` |
| `use_editor_js` | Enables or disables the Editor.js plugin for the field                                            | `True`                   |


### Image uploads

If you want to upload images to the editor then add `django_editorjs_fields.urls` to `urls.py` for your project with `DEBUG=True`:

```python
# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
    path('editorjs/', include('django_editorjs_fields.urls')),
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

In production `DEBUG=False` (use nginx to display images):

```python
# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    ...
    path('editorjs/', include('django_editorjs_fields.urls')),
    ...
]
```

See an example of how you can work with the plugin [here](https://github.com/2ik/django-editorjs-fields/blob/main/example)

## Configure

The application can be configured by editing the project's `settings.py`
file.

| Key                            | Description                                                                     | Default                                                |
| ------------------------------ | ------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `EDITORJS_IMAGE_UPLOAD_PATH`   | Path uploads images                                                             | `settings.MEDIA_URL + 'uploads/images/'`               |
| `EDITORJS_IMAGE_NAME_ORIGINAL` | To use the original name of the image file?                                     | `False`                                                |
| `EDITORJS_IMAGE_NAME_POSTFIX`  | Image file name postfix. Ignored when `EDITORJS_IMAGE_NAME_ORIGINAL` is `True`  | `token_urlsafe(5) # from secrets import token_urlsafe` |
| `EDITORJS_IMAGE_NAME`          | Image file name postfix. Ignored when `EDITORJS_IMAGE_NAME_ORIGINAL` is `False` | `token_urlsafe(8) # from secrets import token_urlsafe` |
| `EDITORJS_VERSION`             | Version Editor.js                                                               | `2.19.0`                                               |

## Support and updates

Use github issues https://github.com/2ik/django-editorjs-fields/issues
