from django.db import models
from django_editorjs_fields import EditorJsJSONField, EditorJsTextField


class Post(models.Model):
    body_default = models.TextField()
    body_editorjs = EditorJsJSONField()
    body_custom = EditorJsJSONField(
        plugins=[
            "@editorjs/image",
            "@editorjs/header",
            "@editorjs/list",
            "editorjs-github-gist-plugin",
            "@editorjs/code",
            "@editorjs/inline-code",
            "@editorjs/table",
        ],
        tools={
            "Gist": {
                "class": "Gist"
            },
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
        blank=True,
    )
    body_textfield = EditorJsTextField(
        plugins=["@editorjs/image"], null=True, blank=True
    )
