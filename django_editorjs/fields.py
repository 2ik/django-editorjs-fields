import traceback

import django
from django.db.models import Field
from django.forms import Textarea

from django_editorjs.widgets import EditorJsWidget

from .config import DEBUG

try:
    # pylint: disable=ungrouped-imports
    from django.db.models import JSONField
except ImportError:
    pass

NEW_VERSION = False

if django.VERSION[0] == 3 and django.VERSION[1] >= 1:
    NEW_VERSION = True


class FieldMixin(Field):
    def get_internal_type(self):
        return "TextField"


class EditorJsFieldMixin:
    def __init__(self, plugins=None, tools=None, **kwargs):
        self.plugins = plugins
        self.tools = tools
        self.version = kwargs.pop('version', '2.18.0')
        self.use_editor_js = kwargs.pop('use_editor_js', True)
        super().__init__(**kwargs)

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


class EditorJsTextField(EditorJsFieldMixin, FieldMixin):
    def __init__(self, plugins=None, tools=None, **kwargs):
        super().__init__(plugins, tools, **kwargs)


class EditorJsJSONField(EditorJsFieldMixin, JSONField if NEW_VERSION else FieldMixin):
    def __init__(self, plugins=None, tools=None, **kwargs):
        if not NEW_VERSION and DEBUG:
            print()
            print('\x1b[0;30;43m {}\x1b[0m'.format(
                'Warning: you don\'t support JSONField, ' +
                'please use EditorJsTextField instead of EditorJsJSONField'
            ))
            print('\x1b[2;34;93m{}\x1b[0m'.format(
                traceback.format_stack()[-3:][0]
            ))
            print()
        super().__init__(plugins, tools, **kwargs)
