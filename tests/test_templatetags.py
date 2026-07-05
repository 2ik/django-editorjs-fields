import json

import pytest
from django.template import Context, Template


@pytest.fixture
def editorjs_context():
    """Render the editorjs template filter"""
    def _render(value):
        t = Template('{% load editorjs %}{{ value|editorjs }}')
        return t.render(Context({'value': value}))
    return _render


class TestEditorJsFilter:
    def test_empty_value(self, editorjs_context):
        assert editorjs_context(None) == ''

    def test_null_string(self, editorjs_context):
        assert editorjs_context('null') == ''

    def test_invalid_json(self, editorjs_context):
        """Invalid JSON is returned as-is"""
        assert editorjs_context('not json at all') == 'not json at all'

    def test_paragraph(self, editorjs_context):
        data = {'blocks': [{'type': 'paragraph', 'data': {'text': 'Hello world'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<p>Hello world</p>' in html

    def test_header(self, editorjs_context):
        data = {'blocks': [{'type': 'header', 'data': {'text': 'Title', 'level': 2}}]}
        html = editorjs_context(json.dumps(data))
        assert '<h2>Title</h2>' in html

    def test_list_unordered(self, editorjs_context):
        data = {'blocks': [{'type': 'list', 'data': {'items': ['a', 'b'], 'style': 'unordered'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<ul>' in html
        assert '<li>a</li>' in html

    def test_list_ordered(self, editorjs_context):
        data = {'blocks': [{'type': 'list', 'data': {'items': ['1', '2'], 'style': 'ordered'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<ol>' in html

    def test_image(self, editorjs_context):
        data = {'blocks': [{'type': 'image', 'data': {
            'file': {'url': 'https://example.com/img.png'},
            'caption': 'test image',
            'stretched': False,
        }}]}
        html = editorjs_context(json.dumps(data))
        assert '<img src="https://example.com/img.png"' in html
        assert 'alt="test image"' in html

    def test_delimiter(self, editorjs_context):
        data = {'blocks': [{'type': 'delimiter', 'data': {}}]}
        html = editorjs_context(json.dumps(data))
        assert '<div class="delimiter"></div>' in html

    def test_quote(self, editorjs_context):
        data = {'blocks': [{'type': 'quote', 'data': {'text': 'Quote text', 'caption': 'Author'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<blockquote' in html
        assert 'Quote text' in html
        assert '<cite>Author</cite>' in html

    def test_code(self, editorjs_context):
        data = {'blocks': [{'type': 'code', 'data': {'code': 'print("hi")'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<pre><code class="code">' in html
        assert '&quot;hi&quot;' in html

    def test_raw(self, editorjs_context):
        data = {'blocks': [{'type': 'raw', 'data': {'html': '<span>raw</span>'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<span>raw</span>' in html

    def test_xss_in_code(self, editorjs_context):
        """HTML tags in code blocks are escaped"""
        data = {'blocks': [{'type': 'code', 'data': {'code': '<div hidden>content</div>'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<div hidden>' not in html
        assert '&lt;div hidden&gt;' in html

    def test_inline_formatting_in_paragraph(self, editorjs_context):
        """Inline formatting from Editor.js is preserved"""
        data = {'blocks': [{'type': 'paragraph', 'data': {'text': 'Hello <b>world</b>'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<b>world</b>' in html

    def test_inline_formatting_in_header(self, editorjs_context):
        """Inline formatting in headers is preserved"""
        data = {'blocks': [{'type': 'header', 'data': {'text': 'Title <i>subtitle</i>', 'level': 2}}]}
        html = editorjs_context(json.dumps(data))
        assert '<i>subtitle</i>' in html

    def test_inline_formatting_in_list(self, editorjs_context):
        """Inline formatting in list items is preserved"""
        data = {'blocks': [{'type': 'list', 'data': {'items': ['<b>bold</b> item'], 'style': 'unordered'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<li><b>bold</b> item</li>' in html

    def test_inline_formatting_in_quote(self, editorjs_context):
        """Inline formatting in quotes is preserved"""
        data = {'blocks': [{'type': 'quote', 'data': {'text': '<u>emphasized</u> quote', 'caption': '<b>Author</b>'}}]}
        html = editorjs_context(json.dumps(data))
        assert '<u>emphasized</u> quote' in html
        assert '<cite><b>Author</b></cite>' in html

    def test_warning(self, editorjs_context):
        data = {'blocks': [{'type': 'warning', 'data': {'title': 'Warn', 'message': 'Be careful'}}]}
        html = editorjs_context(json.dumps(data))
        assert 'class="alert"' in html
        assert 'Warn' in html
        assert 'Be careful' in html

    def test_table(self, editorjs_context):
        data = {'blocks': [{'type': 'table', 'data': {
            'content': [['A', 'B'], ['C', 'D']]
        }}]}
        html = editorjs_context(json.dumps(data))
        assert '<table>' in html
        assert '<tr><td>A</td><td>B</td></tr>' in html

    def test_embed(self, editorjs_context):
        data = {'blocks': [{'type': 'embed', 'data': {
            'service': 'youtube',
            'embed': 'https://www.youtube.com/embed/abc',
            'caption': 'video',
        }}]}
        html = editorjs_context(json.dumps(data))
        assert '<iframe src="https://www.youtube.com/embed/abc"' in html
        assert 'class="embed youtube"' in html

    def test_multiple_blocks(self, editorjs_context):
        data = {'blocks': [
            {'type': 'paragraph', 'data': {'text': 'para'}},
            {'type': 'header', 'data': {'text': 'hdr', 'level': 2}},
        ]}
        html = editorjs_context(json.dumps(data))
        assert '<p>para</p>' in html
        assert '<h2>hdr</h2>' in html

    def test_dict_input(self, editorjs_context):
        """Dict input (JSONField) works without pre-serializing"""
        data = {'blocks': [{'type': 'paragraph', 'data': {'text': 'direct dict'}}]}
        html = editorjs_context(data)
        assert '<p>direct dict</p>' in html

    def test_nbsp_replacement(self, editorjs_context):
        """Actual non-breaking space character passes through"""
        data = {'blocks': [{'type': 'paragraph', 'data': {'text': 'Hello\u00a0World'}}]}
        html = editorjs_context(json.dumps(data))
        assert '\xa0' in html
