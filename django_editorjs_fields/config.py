from datetime import datetime
from secrets import token_urlsafe

from django.conf import settings

DEBUG = getattr(settings, "DEBUG", False)

EDITORJS_IMAGE_UPLOAD_PATH = str(
    getattr(settings, 'EDITORJS_IMAGE_UPLOAD_PATH', 'uploads/images/')
) + datetime.now().strftime("%Y/%m/")

EDITORJS_IMAGE_NAME_ORIGINAL = getattr(settings, "EDITORJS_IMAGE_NAME_ORIGINAL", False)
EDITORJS_IMAGE_NAME_POSTFIX = getattr(
    settings, "EDITORJS_IMAGE_NAME_POSTFIX", token_urlsafe(5)
)
EDITORJS_IMAGE_NAME = getattr(settings, "EDITORJS_IMAGE_NAME", token_urlsafe(8))

DEFAULT_PLUGINS = (
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
