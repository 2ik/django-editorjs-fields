from secrets import token_urlsafe

from django.conf import settings

DEBUG = getattr(settings, "DEBUG", False)

VERSION = getattr(settings, "EDITORJS_VERSION", '2.22.2')

IMAGE_UPLOAD_PATH = str(
    getattr(settings, "EDITORJS_IMAGE_UPLOAD_PATH", 'uploads/images/')
)

IMAGE_UPLOAD_PATH_DATE = getattr(
    settings, "EDITORJS_IMAGE_UPLOAD_PATH_DATE", '%Y/%m/')

IMAGE_NAME_ORIGINAL = getattr(
    settings, "EDITORJS_IMAGE_NAME_ORIGINAL", False)

IMAGE_NAME = getattr(
    settings, "EDITORJS_IMAGE_NAME", lambda **_: token_urlsafe(8))

PLUGINS = getattr(
    settings, "EDITORJS_DEFAULT_PLUGINS", (
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
)

CONFIG_TOOLS = getattr(
    settings, "EDITORJS_DEFAULT_CONFIG_TOOLS", {
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
)

PLUGINS_KEYS = {
    '@editorjs/image': 'Image',
    '@editorjs/header': 'Header',
    '@editorjs/checklist': 'Checklist',
    '@editorjs/list': 'List',
    '@editorjs/quote': 'Quote',
    '@editorjs/raw': 'Raw',
    '@editorjs/code': 'Code',
    '@editorjs/inline-code': 'InlineCode',
    '@editorjs/embed': 'Embed',
    '@editorjs/delimiter': 'Delimiter',
    '@editorjs/warning': 'Warning',
    '@editorjs/link': 'LinkTool',
    '@editorjs/marker': 'Marker',
    '@editorjs/table': 'Table',
}
