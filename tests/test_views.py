import io
import json

from django.test import RequestFactory

from django_editorjs_fields.views import ImageByUrl, ImageUploadView


def _json_response(response):
    return json.loads(response.content)


class TestImageUploadView:
    def _make_image(self, content_type='image/jpeg', name='test.jpg'):
        data = b'\xff\xd8\xff\xe0\x00\x10JFIF'
        return type('FakeFile', (io.BytesIO,), {
            'name': name,
            'content_type': content_type,
        })(data)

    def test_post_valid_image(self):
        factory = RequestFactory()
        request = factory.post('/upload/', {'image': self._make_image()})
        response = ImageUploadView().post(request)
        data = _json_response(response)
        assert data['success'] == 1
        assert 'file' in data

    def test_post_invalid_content_type(self):
        factory = RequestFactory()
        request = factory.post('/upload/', {'image': self._make_image(content_type='text/plain')})
        response = ImageUploadView().post(request)
        assert _json_response(response)['success'] == 0

    def test_post_no_file(self):
        factory = RequestFactory()
        request = factory.post('/upload/', {})
        response = ImageUploadView().post(request)
        assert _json_response(response)['success'] == 0


class TestImageByUrl:
    def test_post_with_url(self):
        factory = RequestFactory()
        request = factory.post(
            '/by_url/',
            data='{"url": "https://example.com/img.png"}',
            content_type='application/json',
        )
        response = ImageByUrl().post(request)
        data = _json_response(response)
        assert data['success'] == 1
        assert data['file']['url'] == 'https://example.com/img.png'

    def test_post_without_url(self):
        factory = RequestFactory()
        request = factory.post('/by_url/', data='{}', content_type='application/json')
        assert _json_response(ImageByUrl().post(request))['success'] == 0

    def test_post_invalid_json(self):
        """Invalid JSON body returns failure instead of 500."""
        factory = RequestFactory()
        request = factory.post('/by_url/', data='not json', content_type='application/json')
        assert _json_response(ImageByUrl().post(request))['success'] == 0

    def test_post_empty_body(self):
        """Empty body returns failure instead of 500."""
        factory = RequestFactory()
        request = factory.post('/by_url/', data='', content_type='application/json')
        assert _json_response(ImageByUrl().post(request))['success'] == 0
