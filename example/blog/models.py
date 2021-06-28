from django.db import models
from django.urls import reverse
from django_editorjs_fields import EditorJsJSONField, EditorJsTextField


class Post(models.Model):
    body_default = models.TextField()
    body_editorjs = EditorJsJSONField(readOnly=False, autofocus=True)
    body_custom = EditorJsJSONField(
        plugins=[
            "@editorjs/image",
            "@editorjs/header",
            "@editorjs/list",
            "editorjs-github-gist-plugin",
            "editorjs-hyperlink",
            "@editorjs/code",
            "@editorjs/inline-code",
            "@editorjs/table@1.3.0",
        ],
        tools={
            "Gist": {
                "class": "Gist"
            },
            "Hyperlink": {
                "class": "Hyperlink",
                "config": {
                    "shortcut": 'CMD+L',
                    "target": '_blank',
                    "rel": 'nofollow',
                    "availableTargets": ['_blank', '_self'],
                    "availableRels": ['author', 'noreferrer'],
                    "validate": False,
                }
            },
            "Image": {
                'class': 'ImageTool',
                "config": {
                    "endpoints": {
                        # Your custom backend file uploader endpoint
                        "byFile": "/editorjs/image_upload/"
                    }
                }
            }
        },
        null=True,
        blank=True,
    )
    body_textfield = EditorJsTextField(  # only images and paragraph (default)
        plugins=["@editorjs/image"], null=True, blank=True,
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
    )

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    def __str__(self):
        return '{}'.format(self.id)
