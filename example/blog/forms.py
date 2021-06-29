from django import forms
from django_editorjs_fields import EditorJsWidget

from .models import Post


class TestForm(forms.ModelForm):
    # body_editorjs = EditorJsWidget(config={"minHeight": 100, 'autofocus': False})

    # inputs = forms.JSONField(widget=EditorJsWidget())
    # inputs.widget.config = {"minHeight": 100}

    class Meta:
        model = Post
        exclude = []
        widgets = {
            'body_editorjs': EditorJsWidget(config={'minHeight': 100}),
            'body_textfield': EditorJsWidget(plugins=[
                "@editorjs/image",
                "@editorjs/header"
            ], config={'minHeight': 100})
        }
