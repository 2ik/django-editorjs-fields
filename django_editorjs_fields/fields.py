from django.core import checks
from django.db.models import Field
from django.forms import Textarea

from .config import DEBUG
from .widgets import EditorJsWidget

try:
    # pylint: disable=ungrouped-imports
    from django.db.models import JSONField  # Django >= 3.1
except ImportError:
    HAS_JSONFIELD = False
else:
    HAS_JSONFIELD = True

__all__ = ['EditorJsTextField', 'EditorJsJSONField']


class FieldMixin(Field):
    def get_internal_type(self):
        return 'TextField'


class EditorJsFieldMixin:
    def __init__(self, plugins=None, tools=None, **kwargs):
        self.plugins = plugins
        self.tools = tools
        self.version = kwargs.pop('version', '2.19.0')
        self.use_editor_js = kwargs.pop('use_editor_js', True)
        super().__init__(**kwargs)

    def formfield(self, **kwargs):
        if self.use_editor_js:
            widget = EditorJsWidget(
                plugins=self.plugins, tools=self.tools, version=self.version
            )
        else:
            widget = Textarea()

        defaults = {'widget': widget}
        defaults.update(kwargs)

        # pylint: disable=no-member
        return super().formfield(**defaults)


class EditorJsTextField(EditorJsFieldMixin, FieldMixin):
    # pylint: disable=useless-super-delegation
    def __init__(self, plugins=None, tools=None, **kwargs):
        super().__init__(plugins, tools, **kwargs)


class EditorJsJSONField(EditorJsFieldMixin, JSONField if HAS_JSONFIELD else FieldMixin):
    # pylint: disable=useless-super-delegation
    def __init__(self, plugins=None, tools=None, **kwargs):
        super().__init__(plugins, tools, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_supported_json())
        return errors

    def _check_supported_json(self):
        if not HAS_JSONFIELD and DEBUG:
            return [
                checks.Warning(
                    'You don\'t support JSONField, please use'
                    'EditorJsTextField instead of EditorJsJSONField',
                    obj=self,
                )
            ]
        return []
