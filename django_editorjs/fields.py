from django.db.models import Field, JSONField
from django.forms import Textarea

from django_editorjs.widgets import EditorJsWidget


class EditorJsFieldMixin:
    def __init__(self, *args, plugins=None, tools=None, **kwargs):
        self.plugins = plugins
        self.tools = tools
        self.version = kwargs.pop('version', '2.18.0')
        self.use_editor_js = kwargs.pop('use_editor_js', True)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if self.use_editor_js:
            widget = EditorJsWidget(
                plugins=self.plugins, tools=self.tools, version=self.version)
        else:
            widget = Textarea()

        defaults = {'widget': widget}
        defaults.update(kwargs)

        # pylint: disable=no-member
        return super().formfield(**defaults)


class EditorJsTextField(EditorJsFieldMixin, Field):
    def get_internal_type(self):
        return "TextField"


class EditorJsJSONField(EditorJsFieldMixin, JSONField):
    pass
