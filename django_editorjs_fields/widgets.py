import json

from django.forms import Media, widgets
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from .config import CONFIG_TOOLS, PLUGINS, VERSION

PLUGINS_KEYS = {
    '@editorjs/image': 'Image',
    '@editorjs/header': 'Header',
    '@editorjs/checklist': 'Checklist',
    '@editorjs/list': 'List',
    '@editorjs/quote': 'Quote',
    '@editorjs/raw': 'Raw',
    '@editorjs/code': 'Code',
    '@editorjs/inline-code': 'InlineCode',
    '@editorjs/embed': 'Embed',
    '@editorjs/delimiter': 'Delimiter',
    '@editorjs/warning': 'Warning',
    '@editorjs/link': 'LinkTool',
    '@editorjs/marker': 'Marker',
    '@editorjs/table': 'Table',
}


class EditorJsWidget(widgets.Textarea):
    def __init__(self, plugins, tools, config=None, **kwargs):
        self.plugins = PLUGINS if plugins is None else plugins
        self.tools = tools or {}
        self.config = config

        super().__init__(**kwargs)

    def get_class_by_key(self, key):
        tool_global = CONFIG_TOOLS.get(key) or {}
        tool_custom = self.tools.get(key) or {}

        return tool_custom.get('class', tool_global.get('class'))

    def configuration(self):
        tools = {}
        custom_tools = self.tools
        # get name packages without version
        plugins = ['@'.join(p.split('@')[:2]) for p in self.plugins]

        for plugin in plugins:
            key = PLUGINS_KEYS.get(plugin)
            original_class = self.get_class_by_key(key)

            if original_class:

                tools[key] = custom_tools.get(
                    key, CONFIG_TOOLS.get(key)
                )

                tools[key]['class'] = original_class

                custom_tools.pop(key, None)

        if custom_tools:
            tools.update(custom_tools)

        self.config.update(tools=tools)
        return self.config

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
        <script>
            initEditorJsField('%s', %s);
        </script>''' % (
            attrs.get('id'),
            json.dumps(self.configuration()),
        )

        return mark_safe(html)
