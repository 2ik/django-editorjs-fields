import json
from re import match

from django.forms import Media, widgets
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from .config import DEFAULT_CONFIG_PLUGINS, DEFAULT_PLUGINS


class EditorJsWidget(widgets.Textarea):
    def __init__(self, version, plugins=None, tools=None, **kwargs):
        self.version = version
        self.plugins = DEFAULT_PLUGINS if plugins is None else plugins
        self.tools = tools or {}
        super().__init__(**kwargs)

    @cached_property
    def media(self):
        plugins = self.plugins
        custom_tools = self.tools
        _tools = {}

        for name, config in DEFAULT_CONFIG_PLUGINS.items():
            matches = filter(lambda v, n=name: match(rf'{n}($|@)', v), plugins)
            if list(matches):
                _tools.update(config)

        for key, config in custom_tools.items():
            if key in _tools:
                _tools[key].update(config)
            else:
                _tools[key] = config

        self.tools = _tools

        js_list = [
            '//cdn.jsdelivr.net/npm/@editorjs/editorjs@'
            + self.version  # default plugin
        ]

        if plugins:
            js_list += ['//cdn.jsdelivr.net/npm/' + p for p in plugins]

        js_list.append('django-editorjs-fields/js/django-editorjs-fields.js')

        return Media(
            css={'all': ['django-editorjs-fields/css/django-editorjs-fields.css']},
            js=js_list,
        )

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs)

        html += '''
        <div data-editorjs-holder></div>
        <script>
            initEditorJsField('%s', %s);
        </script>''' % (
            attrs.get('id'),
            json.dumps(self.tools),
        )

        return mark_safe(html)
