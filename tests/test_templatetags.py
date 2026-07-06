import json

import pytest
from django.template import Context, Template


@pytest.fixture
def render_editorjs():
    """Render the editorjs template filter."""
    t = Template('{% load editorjs %}{{ value|editorjs }}')
    return lambda v: t.render(Context({'value': v}))


def _block(type_, data):
    return {'type': type_, 'data': data}


class TestEditorJsFilter:
    def test_empty_value(self, render_editorjs):
        assert render_editorjs(None) == ''

    def test_null_string(self, render_editorjs):
        assert render_editorjs('null') == ''

    def test_invalid_json(self, render_editorjs):
        assert render_editorjs('not json at all') == 'not json at all'

    def test_paragraph(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('paragraph', {'text': 'Hello world'})]}))
        assert '<p>Hello world</p>' in html

    def test_header(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('header', {'text': 'Title', 'level': 2})]}))
        assert '<h2>Title</h2>' in html

    def test_list_unordered(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('list', {'items': ['a', 'b'], 'style': 'unordered'})]}))
        assert '<ul>' in html
        assert '<li>a</li>' in html

    def test_list_ordered(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('list', {'items': ['1', '2'], 'style': 'ordered'})]}))
        assert '<ol>' in html

    def test_list_with_dict_items(self, render_editorjs):
        """List items as dicts with 'content' key (Editor.js 2.x format)."""
        items = [
            {'meta': {}, 'items': [], 'content': 'one'},
            {'meta': {}, 'items': [], 'content': 'two'},
        ]
        html = render_editorjs(json.dumps({'blocks': [_block('list', {'items': items, 'style': 'ordered'})]}))
        assert '<li>one</li>' in html
        assert '<li>two</li>' in html

    def test_image(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('image', {
            'file': {'url': 'https://example.com/img.png'},
            'caption': 'test image',
            'stretched': False,
        })]}))
        assert 'src="https://example.com/img.png"' in html
        assert 'alt="test image"' in html

    def test_delimiter(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('delimiter', {})]}))
        assert '<div class="delimiter"></div>' in html

    def test_quote(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('quote', {'text': 'Quote text', 'caption': 'Author'})]}))
        assert 'Quote text' in html
        assert '<cite>Author</cite>' in html

    def test_quote_without_alignment(self, render_editorjs):
        """Quote without alignment must not render class="None"."""
        html = render_editorjs(json.dumps({'blocks': [_block('quote', {'text': 'text'})]}))
        assert 'None' not in html

    def test_quote_with_alignment(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('quote', {'text': 't', 'alignment': 'right'})]}))
        assert 'align-right' in html

    def test_code(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('code', {'code': 'print("hi")'})]}))
        assert '<pre><code class="code">' in html
        assert 'print("hi")' in html

    def test_code_preserves_html_tags(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('code', {'code': '<div>hello</div>'})]}))
        assert '<div>hello</div>' in html

    def test_raw(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('raw', {'html': '<span>raw</span>'})]}))
        assert '<span>raw</span>' in html

    def test_warning(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('warning', {'title': 'Warn', 'message': 'Careful'})]}))
        assert 'class="alert"' in html
        assert 'Warn' in html

    def test_table(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('table', {'content': [['A', 'B'], ['C', 'D']]})]}))
        assert '<tr><td>A</td><td>B</td></tr>' in html

    def test_embed(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('embed', {
            'service': 'youtube',
            'embed': 'https://www.youtube.com/embed/abc',
            'caption': 'video',
        })]}))
        assert 'src="https://www.youtube.com/embed/abc"' in html
        assert 'class="embed youtube"' in html

    def test_linktool(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('linktool', {
            'link': 'https://example.com',
            'meta': {'title': 'Example', 'description': 'Desc', 'image': None},
        })]}))
        assert 'href="https://example.com"' in html
        assert 'Example' in html

    def test_linktool_with_null_image(self, render_editorjs):
        """Link with null image must not crash."""
        html = render_editorjs(json.dumps({'blocks': [_block('linktool', {
            'link': 'https://example.com',
            'meta': {'title': 'T', 'image': None},
        })]}))
        assert 'href="https://example.com"' in html

    # --- Inline formatting preservation ---

    def test_inline_formatting_in_paragraph(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('paragraph', {'text': 'Hello <b>world</b>'})]}))
        assert '<b>world</b>' in html

    def test_inline_formatting_in_header(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('header', {'text': 'T <i>s</i>', 'level': 2})]}))
        assert '<i>s</i>' in html

    def test_inline_formatting_in_list(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('list', {'items': ['<b>bold</b> item'], 'style': 'unordered'})]}))
        assert '<li><b>bold</b> item</li>' in html

    def test_inline_formatting_in_quote(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('quote', {'text': '<u>emph</u> q', 'caption': '<b>A</b>'})]}))
        assert '<u>emph</u> q' in html
        assert '<cite><b>A</b></cite>' in html

    # --- Misc ---

    def test_multiple_blocks(self, render_editorjs):
        blocks = [
            _block('paragraph', {'text': 'para'}),
            _block('header', {'text': 'hdr', 'level': 2}),
        ]
        html = render_editorjs(json.dumps({'blocks': blocks}))
        assert '<p>para</p>' in html
        assert '<h2>hdr</h2>' in html

    def test_dict_input(self, render_editorjs):
        """Dict input (JSONField) works without pre-serializing."""
        html = render_editorjs({'blocks': [_block('paragraph', {'text': 'direct dict'})]})
        assert '<p>direct dict</p>' in html

    def test_nbsp_replacement(self, render_editorjs):
        html = render_editorjs(json.dumps({'blocks': [_block('paragraph', {'text': 'Hello\u00a0World'})]}))
        assert '\xa0' in html
