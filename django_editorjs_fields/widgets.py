import json

from django.forms import Media, widgets
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from .config import CONFIG_TOOLS, PLUGINS, PLUGINS_KEYS, VERSION


class EditorJsWidget(widgets.Textarea):
    def __init__(self, plugins=None, tools=None, config=None, **kwargs):
        self.plugins = PLUGINS if plugins is None else plugins
        self.tools = tools
        self.config = config

        widget = kwargs.pop('widget', None) # Fix "__init__() got an unexpected keyword argument 'widget'"
        if widget:
            self.plugins = widget.plugins
            self.tools = widget.tools
            self.config = widget.config

        super().__init__(**kwargs)

    def configuration(self):
        tools = {}
        config = self.config or {}
        custom_tools = self.tools or {}
        # get name packages without version
        plugins = ['@'.join(p.split('@')[:2]) for p in self.plugins]

        for plugin in plugins:
            plugin_key = PLUGINS_KEYS.get(plugin)
            plugin_tools = custom_tools.get(
                plugin_key) or CONFIG_TOOLS.get(plugin_key) or {}
            plugin_class = plugin_tools.get('class')

            if plugin_class:

                tools[plugin_key] = custom_tools.get(
                    plugin_key, CONFIG_TOOLS.get(plugin_key)
                )

                tools[plugin_key]['class'] = plugin_class

                custom_tools.pop(plugin_key, None)

        if custom_tools:
            tools.update(custom_tools)

        config.update(tools=tools)
        return config

    @cached_property
    def media(self):
        js_list = [
            '//cdn.jsdelivr.net/npm/@editorjs/editorjs@' + VERSION  # lib
        ]
        js_list += ['//cdn.jsdelivr.net/npm/' + p for p in self.plugins or []]
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
        html = super().render(name, value, attrs)

        html += '''
        <div data-editorjs-holder></div>
        <script defer>
        addEventListener('DOMContentLoaded', function () {
            initEditorJsField('%s', %s);
        })
        </script>''' % (
            attrs.get('id'),
            json.dumps(self.configuration()),
        )

        return mark_safe(html)
