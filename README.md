# Editor.js for Django

Django plugin for using [Editor.js](https://editorjs.io/)

> This plugin works fine with JSONField in Django >= 3.1

[![Django Editor.js](https://i.ibb.co/r6xt4HJ/image.png)](https://github.com/2ik/django-editorjs-fields)

[![Python versions](https://img.shields.io/pypi/pyversions/django-editorjs-fields)](https://pypi.org/project/django-editorjs-fields/)
[![Python versions](https://img.shields.io/pypi/djversions/django-editorjs-fields)](https://pypi.org/project/django-editorjs-fields/)
[![Downloads](https://static.pepy.tech/personalized-badge/django-editorjs-fields?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/django-editorjs-fields)

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

## Upgrade

```bash
pip install django-editorjs-fields --upgrade
python manage.py collectstatic  # upgrade js and css files
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

#### New in version 0.2.1. Django Templates support

```html
<!-- template.html -->

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    {% load editorjs %} 
    {{ post.body_default }}
    {{ post.body_editorjs | editorjs}}
    {{ post.body_editorjs_text | editorjs}}
  </body>
</html>
```

## Additionally

You can add custom Editor.js plugins and configs ([List plugins](https://github.com/editor-js/awesome-editorjs))

Example custom field in models.py

```python
# models.py
from django.db import models
from django_editorjs_fields import EditorJsJSONField


class Post(models.Model):
    body_editorjs_custom = EditorJsJSONField(
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
            "Gist": {
                "class": "Gist"  # Include the plugin class. See docs Editor.js plugins
            },
            "Image": {
                "config": {
                    "endpoints": {
                        "byFile": "/editorjs/image_upload/"  # Your custom backend file uploader endpoint
                    }
                }
            }
        },
        i18n={
            'messages': {
                'blockTunes': {
                    "delete": {
                        "Delete": "Удалить"
                    },
                    "moveUp": {
                        "Move up": "Переместить вверх"
                    },
                    "moveDown": {
                        "Move down": "Переместить вниз"
                    }
                }
            },
        }
        null=True,
        blank=True
    )

```

**django-editorjs-fields** support this list of Editor.js plugins by default:
<a name="plugins"></a>

<details>
    <summary>EDITORJS_DEFAULT_PLUGINS</summary>

```python
EDITORJS_DEFAULT_PLUGINS = (
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
)
```

</details>

<details>
    <summary>EDITORJS_DEFAULT_CONFIG_TOOLS</summary>

```python
EDITORJS_DEFAULT_CONFIG_TOOLS = {
    'Image': {
        'class': 'ImageTool',
        'inlineToolbar': True,
        "config": {"endpoints": {"byFile": "/editorjs/image_upload/"}},
    },
    'Header': {
        'class': 'Header',
        'inlineToolbar': True,
        'config': {
            'placeholder': 'Enter a header',
            'levels': [2, 3, 4],
            'defaultLevel': 2,
        }
    },
    'Checklist': {'class': 'Checklist', 'inlineToolbar': True},
    'List': {'class': 'List', 'inlineToolbar': True},
    'Quote': {'class': 'Quote', 'inlineToolbar': True},
    'Raw': {'class': 'RawTool'},
    'Code': {'class': 'CodeTool'},
    'InlineCode': {'class': 'InlineCode'},
    'Embed': {'class': 'Embed'},
    'Delimiter': {'class': 'Delimiter'},
    'Warning': {'class': 'Warning', 'inlineToolbar': True},
    'LinkTool': {'class': 'LinkTool'},
    'Marker': {'class': 'Marker', 'inlineToolbar': True},
    'Table': {'class': 'Table', 'inlineToolbar': True},
}
```

</details>

`EditorJsJSONField` accepts all the arguments of `JSONField` class.

`EditorJsTextField` accepts all the arguments of `TextField` class.

Additionally, it includes arguments such as:

| Args            | Description                                                                                                                                  | Default                         |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| `plugins`       | List plugins Editor.js                                                                                                                       | `EDITORJS_DEFAULT_PLUGINS`      |
| `tools`         | Map of Tools to use. Set config `tools` for Editor.js [See docs](https://editorjs.io/configuration#passing-saved-data)                       | `EDITORJS_DEFAULT_CONFIG_TOOLS` |
| `use_editor_js` | Enables or disables the Editor.js plugin for the field                                                                                       | `True`                          |
| `autofocus`     | If true, set caret at the first Block after Editor is ready                                                                                  | `False`                         |
| `hideToolbar`   | If true, toolbar won't be shown                                                                                                              | `False`                         |
| `inlineToolbar` | Defines default toolbar for all tools.                                                                                                       | `True`                          |
| `readOnly`      | Enable read-only mode                                                                                                                        | `False`                         |
| `minHeight`     | Height of Editor's bottom area that allows to set focus on the last Block                                                                    | `300`                           |
| `logLevel`      | Editors log level (how many logs you want to see)                                                                                            | `ERROR`                         |
| `placeholder`   | First Block placeholder                                                                                                                      | `Type text...`                  |
| `defaultBlock`  | This Tool will be used as default. Name should be equal to one of Tool`s keys of passed tools. If not specified, Paragraph Tool will be used | `paragraph`                     |
| `i18n`          | Internalization config                                                                                                                       | `{}`                            |
| `sanitizer`     | Define default sanitizer configuration                                                                                                       | `{ p: true, b: true, a: true }` |

## Image uploads

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

## Forms

```python
from django import forms
from django_editorjs_fields import EditorJsWidget


class TestForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = []
        widgets = {
            'body_editorjs': EditorJsWidget(config={'minHeight': 100}),
            'body_editorjs_text': EditorJsWidget(plugins=["@editorjs/image", "@editorjs/header"])
        }
```

## Theme

### Default Theme

![image](https://user-images.githubusercontent.com/6692517/124242133-7a7dad00-db2d-11eb-812f-84a5c44e88c9.png)

### Dark Theme

plugin use css property [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) to define a dark theme in browser

![image](https://user-images.githubusercontent.com/6692517/124240864-3dfd8180-db2c-11eb-85c1-21f0faf41775.png)

## Configure

The application can be configured by editing the project's `settings.py`
file.

| Key                               | Description                                                            | Default               | Type                                                                                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EDITORJS_DEFAULT_PLUGINS`        | List of plugins names Editor.js from npm                               | [See above](#plugins) | `list[str]`, `tuple[str]`                                                                                                                               |
| `EDITORJS_DEFAULT_CONFIG_TOOLS`   | Map of Tools to use                                                    | [See above](#plugins) | `dict[str, dict]`                                                                                                                                       |
| `EDITORJS_IMAGE_UPLOAD_PATH`      | Path uploads images                                                    | `uploads/images/`     | `str`                                                                                                                                                   |
| `EDITORJS_IMAGE_UPLOAD_PATH_DATE` | Subdirectories                                                         | `%Y/%m/`              | `str`                                                                                                                                                   |
| `EDITORJS_IMAGE_NAME_ORIGINAL`    | To use the original name of the image file?                            | `False`               | `bool`                                                                                                                                                  |
| `EDITORJS_IMAGE_NAME`             | Image file name. Ignored when `EDITORJS_IMAGE_NAME_ORIGINAL` is `True` | `token_urlsafe(8)`    | `callable(filename: str, file: InMemoryUploadedFile)` ([docs](https://docs.djangoproject.com/en/3.0/ref/files/uploads/)) |
| `EDITORJS_VERSION`                | Version Editor.js                                                      | `2.22.3`              | `str`                                                                                                                                                   |

For `EDITORJS_IMAGE_NAME` was used `from secrets import token_urlsafe`

## Support and updates

Use github issues https://github.com/2ik/django-editorjs-fields/issues
