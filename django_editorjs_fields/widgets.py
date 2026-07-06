
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import Media, widgets
from django.forms.renderers import get_default_renderer
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

try:
    from django.utils.functional import cached_property
except ImportError:
    from functools import cached_property

from .config import CONFIG_TOOLS, PLUGINS, PLUGINS_KEYS, VERSION


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


json_encode = LazyEncoder().encode


class EditorJsWidget(widgets.Textarea):
    def __init__(self, plugins=None, tools=None, config=None, **kwargs):
        self.plugins = plugins
        self.tools = tools
        self.config = config

        # Fix "__init__() got an unexpected keyword argument 'widget'"
        widget = kwargs.pop('widget', None)
        if widget:
            self.plugins = widget.plugins
            self.tools = widget.tools
            self.config = widget.config

        super().__init__(**kwargs)

    def configuration(self):
        config = dict(self.config) if self.config else {}

        if self.plugins or self.tools:
            tools = self._build_tools()
        else:
            tools = dict(CONFIG_TOOLS)

        config['tools'] = tools
        return config

    def _build_tools(self):
        tools = {}
        custom_tools = dict(self.tools) if self.tools else {}

        # Strip versions: '@editorjs/header@2.7.0' -> '@editorjs/header'
        plugins = ['@'.join(p.split('@')[:2]) for p in self.plugins or PLUGINS]

        for plugin in plugins:
            plugin_key = PLUGINS_KEYS.get(plugin)
            if not plugin_key:
                continue

            entry = custom_tools.get(plugin_key) or CONFIG_TOOLS.get(plugin_key)
            if not entry or 'class' not in entry:
                continue

            tools[plugin_key] = dict(entry)
            tools[plugin_key]['class'] = entry['class']
            custom_tools.pop(plugin_key, None)

        tools.update(custom_tools)
        return tools

    @cached_property
    def media(self):
        js_list = [
            '//cdn.jsdelivr.net/npm/@editorjs/editorjs@' + VERSION  # lib
        ]

        plugins = self.plugins or PLUGINS

        if plugins:
            js_list += [p if p.startswith('https://') else ('//cdn.jsdelivr.net/npm/' + p) for p in plugins]

        js_list.append('django-editorjs-fields/js/django-editorjs-fields.js')

        return Media(
            js=js_list,
            css={
                'all': [
                    'django-editorjs-fields/css/django-editorjs-fields.css'
                ]
            },
        )

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        if renderer is None:
            renderer = get_default_renderer()

        return mark_safe(renderer.render("django-editorjs-fields/widget.html", {
            'widget': {
                'name': name,
                'value': conditional_escape(force_str(value)),
                'attrs': self.build_attrs(self.attrs, attrs),
                'config': json_encode(self.configuration()),
            }
        }))
