from django import forms
from django_editorjs_fields import EditorJsWidget

from .models import Post


class TestForm(forms.ModelForm):
    body_editorjs = EditorJsWidget()

    inputs = forms.JSONField(widget=EditorJsWidget())
    inputs.widget.config = {"minHeight": 100}

    class Meta:
        model = Post
        fields = ['body_textfield', 'body_editorjs']
        widgets = {
            'body_textfield': EditorJsWidget(
                config={'minHeight': 100},
                plugins=[
                    "@editorjs/image",
                    "@editorjs/header"
                ])
        }
