import json

import pytest
from django.core.exceptions import ValidationError

from django_editorjs_fields import EditorJsJSONField, EditorJsTextField


@pytest.mark.django_db
class TestEditorJsTextField:
    def test_clean_null_string_becomes_none(self):
        """'null' string becomes None (with null=True, blank=True)"""
        field = EditorJsTextField(null=True, blank=True)
        result = field.clean('null', None)
        assert result is None

    def test_clean_valid_json_with_allowed_embed(self):
        """Valid JSON with allowed hostname passes"""
        data = {
            'blocks': [
                {
                    'type': 'embed',
                    'data': {'embed': 'https://www.youtube.com/watch?v=test'}
                }
            ]
        }
        field = EditorJsTextField()
        result = field.clean(json.dumps(data), None)
        assert result is not None

    def test_clean_rejects_disallowed_embed(self):
        """Embed with disallowed hostname raises ValidationError"""
        data = {
            'blocks': [
                {
                    'type': 'embed',
                    'data': {'embed': 'https://evil.com/embed/123'}
                }
            ]
        }
        field = EditorJsTextField()
        with pytest.raises(ValidationError, match='evil.com'):
            field.clean(json.dumps(data), None)

    def test_clean_plain_text_unchanged(self):
        """Plain text (not JSON) passes through"""
        field = EditorJsTextField()
        result = field.clean('some plain text', None)
        assert result == 'some plain text'

    def test_clean_non_embed_blocks_pass(self):
        """Non-embed blocks don't trigger validation"""
        data = {
            'blocks': [
                {'type': 'paragraph', 'data': {'text': 'hello'}}
            ]
        }
        field = EditorJsTextField()
        result = field.clean(json.dumps(data), None)
        assert result is not None

    def test_formfield_returns_editorjs_widget(self):
        """formfield returns EditorJsWidget by default"""
        field = EditorJsTextField()
        ff = field.formfield()
        assert ff.widget.__class__.__name__ == 'EditorJsWidget'

    def test_formfield_use_editorjs_false(self):
        """use_editorjs=False returns Textarea widget"""
        field = EditorJsTextField(use_editorjs=False)
        ff = field.formfield()
        from django.forms import Textarea
        assert isinstance(ff.widget, Textarea)

    def test_formfield_passes_plugins_and_tools(self):
        """plugins and tools are forwarded to the widget"""
        plugins = ['@editorjs/header']
        tools = {'Header': {'class': 'Header'}}
        field = EditorJsTextField(plugins=plugins, tools=tools)
        ff = field.formfield()
        assert ff.widget.plugins == plugins
        assert ff.widget.tools == tools


@pytest.mark.django_db
class TestEditorJsJSONField:
    def test_clean_dict_value(self):
        """Dict value with allowed embed passes"""
        data = {
            'blocks': [
                {
                    'type': 'embed',
                    'data': {'embed': 'https://www.youtube.com/watch?v=test'}
                }
            ]
        }
        field = EditorJsJSONField()
        result = field.clean(data, None)
        assert result is not None

    def test_clean_rejects_disallowed_embed_dict(self):
        """Dict with disallowed embed raises ValidationError"""
        data = {
            'blocks': [
                {
                    'type': 'embed',
                    'data': {'embed': 'https://evil.com/x'}
                }
            ]
        }
        field = EditorJsJSONField()
        with pytest.raises(ValidationError):
            field.clean(data, None)

    def test_clean_none_with_null_true(self):
        """None value is skipped when null=True, blank=True"""
        field = EditorJsJSONField(null=True, blank=True)
        result = field.clean(None, None)
        assert result is None

    def test_get_internal_type(self):
        field = EditorJsJSONField()
        assert field.get_internal_type() in ('JSONField', 'TextField')
