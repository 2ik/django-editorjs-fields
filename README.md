# django-editorjs-fields

Django integration for [Editor.js](https://editorjs.io/) — a block-style WYSIWYG editor.

- **Django:** 2.2 – 6.x
- **Python:** 3.8 – 3.13
- **Editor.js:** 2.31.6
- [![PyPI Downloads](https://static.pepy.tech/personalized-badge/django-editorjs-fields?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/django-editorjs-fields)

---

[![Django Editor.js](https://i.ibb.co/r6xt4HJ/image.png)](https://github.com/2ik/django-editorjs-fields)

---

## Table of Contents

- [Installation](#installation)
- [Quick start](#quick-start)
- [Rendering in templates](#rendering-in-templates)
- [Field arguments](#field-arguments)
- [Custom plugins](#custom-plugins)
- [Forms and widgets](#forms-and-widgets)
- [Image uploads](#image-uploads)
- [Dark theme](#dark-theme)
- [Settings](#settings)
- [Support](#support)

---

## Installation

```bash
pip install django-editorjs-fields
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_editorjs_fields',
]
```

### Upgrade

```bash
pip install django-editorjs-fields --upgrade
python manage.py collectstatic
```

---

## Quick start

Define fields in your model:

```python
from django.db import models
from django_editorjs_fields import EditorJsJSONField, EditorJsTextField


class Post(models.Model):
    # Stores data as JSON (Django >= 3.1)
    body = EditorJsJSONField(null=True, blank=True)

    # Stores data as serialized JSON string (any Django version)
    body_text = EditorJsTextField(null=True, blank=True)
```

Don't forget to add URLs for image upload and link metadata:

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    # ...
    path('editorjs/', include('django_editorjs_fields.urls')),
]
```

See the full example project: [`example/`](https://github.com/2ik/django-editorjs-fields/tree/main/example)

---

## Rendering in templates

Use the `editorjs` template filter to render stored blocks as HTML:

```html
{% load editorjs %}
{{ post.body|editorjs }}
```

The filter escapes all user content to prevent XSS. Use the `raw` block type if you need to render trusted HTML.

---

## Field arguments

Both `EditorJsJSONField` and `EditorJsTextField` accept all arguments of their base Django fields (`JSONField` / `TextField`) plus:

| Argument        | Description                                                                             | Default   |
| --------------- | --------------------------------------------------------------------------------------- | --------- |
| `plugins`       | List of Editor.js plugin packages                                                       | `EDITORJS_DEFAULT_PLUGINS` |
| `tools`         | Tool configuration map ([docs](https://editorjs.io/configuration#passing-saved-data))   | `EDITORJS_DEFAULT_CONFIG_TOOLS` |
| `config`        | Editor.js config overrides (`autofocus`, `readOnly`, `placeholder`, etc.)   | `{}`      |

Config keys are passed directly to the Editor.js constructor. Refer to the [official docs](https://github.com/codex-team/editor.js/blob/v2.31.6/types/configs/editor-config.d.ts) for all options.

---

## Custom plugins

Pass a custom plugin list and tool configuration to the field:

```python
body = EditorJsJSONField(
    plugins=[
        "@editorjs/image",
        "@editorjs/header",
        "@editorjs/code@2.6.0",      # pin a specific version
        "@editorjs/list@latest",
        # Full URLs work for plugins hosted outside npm/jsDelivr
        "https://cdn.jsdelivr.net/gh/some-repo/plugin@main/index.js",
    ],
    tools={
        "Image": {
            "config": {
                "endpoints": {
                    "byFile": "/my-upload-endpoint/"
                }
            }
        },
    },
    config={"minHeight": 500},
)
```

### Registering custom plugin keys

If your custom plugin is not in the built-in `PLUGINS_KEYS` map, register it in settings:

```python
# settings.py
EDITORJS_PLUGINS_KEYS = {
    'my/custom-plugin': 'MyCustomPlugin',
}
```

This map is merged with built-in defaults — you only need entries for your own plugins.

### Built-in plugins

The following plugins are enabled by default:

<details>
    <summary>EDITORJS_DEFAULT_PLUGINS</summary>

```python
(
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
{
    'Image': {
        'class': 'ImageTool',
        'inlineToolbar': True,
        "config": {
            "endpoints": {
                "byFile": reverse_lazy('editorjs_image_upload'),
                "byUrl": reverse_lazy('editorjs_image_by_url')
            }
        },
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
    'List': {'class': 'EditorjsList', 'inlineToolbar': True},
    'Quote': {'class': 'Quote', 'inlineToolbar': True},
    'Raw': {'class': 'RawTool'},
    'Code': {'class': 'CodeTool'},
    'InlineCode': {'class': 'InlineCode'},
    'Embed': {'class': 'Embed'},
    'Delimiter': {'class': 'Delimiter'},
    'Warning': {'class': 'Warning', 'inlineToolbar': True},
    'LinkTool': {
        'class': 'LinkTool',
        'config': {
            'endpoint': reverse_lazy('editorjs_linktool'),
        }
    },
    'Marker': {'class': 'Marker', 'inlineToolbar': True},
    'Table': {'class': 'Table', 'inlineToolbar': True},
}
```

</details>

---

## Forms and widgets

Use `EditorJsWidget` in forms:

```python
from django import forms
from django_editorjs_fields import EditorJsWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': EditorJsWidget(
                plugins=["@editorjs/image", "@editorjs/header"],
                config={'minHeight': 200},
            )
        }
```

---

## Image uploads

Include the package URLs (see [Quick start](#quick-start)). Images are saved to `MEDIA_ROOT/uploads/images/YYYY/MM/` by default.

In development (`DEBUG=True`), also serve media files:

```python
# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

In production, configure your web server (nginx, Apache) to serve `MEDIA_URL`.

---

## Dark theme

The editor adapts to the system dark mode via `prefers-color-scheme`. In Django admin (4.2+), it also respects the theme toggle button (`data-theme="dark"`).

---

## Settings

All settings go in your project's `settings.py`.

| Setting                             | Description                                                    | Default                                          | Type                     |
| ----------------------------------- | -------------------------------------------------------------- | ------------------------------------------------ | ------------------------ |
| `EDITORJS_DEFAULT_PLUGINS`          | Plugin package list                                            | [See above](#built-in-plugins)                   | `list`, `tuple`          |
| `EDITORJS_DEFAULT_CONFIG_TOOLS`     | Tool configuration map                                         | [See above](#built-in-plugins)                   | `dict`                   |
| `EDITORJS_PLUGINS_KEYS`             | Custom plugin → tool key map (merged with defaults)            | `{}`                                             | `dict`                   |
| `EDITORJS_VERSION`                  | Editor.js version                                              | `'2.31.6'`                                       | `str`                    |
| `EDITORJS_IMAGE_UPLOAD_PATH`        | Base upload directory                                          | `'uploads/images/'`                              | `str`                    |
| `EDITORJS_IMAGE_UPLOAD_PATH_DATE`   | Date subdirectory format                                       | `'%Y/%m/'`                                       | `str`                    |
| `EDITORJS_IMAGE_NAME_ORIGINAL`      | Keep original filename                                         | `False`                                          | `bool`                   |
| `EDITORJS_IMAGE_NAME`               | Filename generator callable                                    | `token_urlsafe(8)`                               | `callable`               |
| `EDITORJS_EMBED_HOSTNAME_ALLOWED`   | Allowed hostnames for embed validation                         | See source                                       | `list`, `tuple`          |

---

## Support

Report issues on [GitHub](https://github.com/2ik/django-editorjs-fields/issues)
