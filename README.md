# Editor.js for Django

Django plugin for using [Editor.js](https://editorjs.io/)

> This plugin works fine with JSONField in Django >= 3.1

## Installation

```bash
pip install django-editorjs
```

Add django_editorjs to INSTALLED_APPS in settings.py for your project:
```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_editorjs',
]
```

## Usage

Add code in your model
```python
# models.py
from django.db import models
from django_editorjs import EditorJsJSONField, EditorJsTextField  # import


class Post(models.Model):
    body_default = models.TextField()
    body_editorjs = EditorJsJSONField()  # Django >= 3.1
    body_editorjs_text = EditorJsTextField()  # Django <= 3.0

```

Or add custom Editor.js plugins and configs ([List plugins](https://github.com/editor-js/awesome-editorjs))

```python
# models.py
from django.db import models
from django_editorjs import EditorJsJSONField, EditorJsTextField  # import


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

If you want to upload images to the editor then add django_editorjs.urls to urls.py for your project:
```python
# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('editorjs/', include('django_editorjs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

See an example of how you can work with the plugin [here](https://github.com/2ik/django-editorjs/blob/main/example)


## Support and updates

Use github issues https://github.com/2ik/django-editorjs/issues