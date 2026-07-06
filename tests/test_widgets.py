
from django_editorjs_fields.config import CONFIG_TOOLS
from django_editorjs_fields.widgets import EditorJsWidget


class TestEditorJsWidget:
    def test_configuration_default_tools(self):
        """Default config contains all tools from CONFIG_TOOLS"""
        widget = EditorJsWidget()
        config = widget.configuration()
        assert 'tools' in config
        for key in CONFIG_TOOLS:
            assert key in config['tools']

    def test_configuration_custom_plugins(self):
        """Custom plugins filter the tools"""
        widget = EditorJsWidget(plugins=['@editorjs/header', '@editorjs/list'])
        config = widget.configuration()
        assert 'Header' in config['tools']
        assert 'List' in config['tools']
        # Image should not be present (not in custom plugins)
        assert 'Image' not in config['tools']

    def test_configuration_custom_tools_override(self):
        """Custom tools override defaults"""
        tools = {'Header': {'class': 'Header', 'config': {'defaultLevel': 3}}}
        widget = EditorJsWidget(tools=tools)
        config = widget.configuration()
        # When self.tools is set but self.plugins is None, it still uses CONFIG_TOOLS
        # but merges custom_tools — let's verify Header has the override
        header_tool = config['tools'].get('Header', {})
        assert header_tool.get('config', {}).get('defaultLevel') == 3

    def test_configuration_with_plugins_and_custom_tools(self):
        """Plugins + custom tools work together"""
        plugins = ['@editorjs/header']
        tools = {
            'Gist': {'class': 'Gist'}
        }
        widget = EditorJsWidget(plugins=plugins, tools=tools)
        config = widget.configuration()
        assert 'Header' in config['tools']
        assert 'Gist' in config['tools']

    def test_media_js_includes_editorjs(self):
        """Media JS includes Editor.js CDN link"""
        widget = EditorJsWidget()
        media = widget.media
        assert any('editorjs' in js.lower() for js in media._js)

    def test_media_js_includes_plugins(self):
        """Media JS includes plugin scripts"""
        widget = EditorJsWidget()
        media = widget.media
        js_urls = ' '.join(media._js)
        assert '@editorjs/paragraph' in js_urls

    def test_media_css_includes_stylesheet(self):
        """Media CSS includes the stylesheet"""
        widget = EditorJsWidget()
        media = widget.media
        css_all = ''.join(media.render_css())
        assert 'django-editorjs-fields.css' in css_all

    def test_render_returns_html(self):
        """render returns valid HTML with textarea and holder"""
        widget = EditorJsWidget()
        html = widget.render('test_field', '', attrs={'id': 'id_test_field'})
        assert 'textarea' in html
        assert 'data-editorjs-textarea' in html
        assert 'id_test_field_editorjs_holder' in html

    def test_render_with_json_value(self):
        """render passes JSON value through safely"""
        value = '{"blocks":[{"type":"paragraph","data":{"text":"hello"}}]}'
        widget = EditorJsWidget()
        html = widget.render('test_field', value, attrs={'id': 'id_test_field'})
        assert 'hello' in html

    def test_render_none_value(self):
        """render handles None value"""
        widget = EditorJsWidget()
        html = widget.render('test_field', None, attrs={'id': 'id_test_field'})
        assert 'textarea' in html

    def test_configuration_passes_config_dict(self):
        """Custom config options are merged into the result"""
        widget = EditorJsWidget(config={'autofocus': True, 'minHeight': 400})
        config = widget.configuration()
        assert config['autofocus'] is True
        assert config['minHeight'] == 400

    def test_widget_keyword_arg_fix(self):
        """widget= keyword is handled without crashing (Django admin passes it)"""
        base = EditorJsWidget(plugins=['@editorjs/header'])
        widget = EditorJsWidget(widget=base)
        assert widget.plugins == ['@editorjs/header']
