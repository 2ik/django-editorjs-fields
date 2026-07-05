import io
import json

from django_editorjs_fields.views import ImageByUrl, ImageUploadView


def _json_response(response):
    return json.loads(response.content)


class TestImageUploadView:
    def _make_image(self, content_type='image/jpeg', name='test.jpg'):
        data = b'\xff\xd8\xff\xe0\x00\x10JFIF'  # minimal JPEG header
        return type('FakeFile', (io.BytesIO,), {
            'name': name,
            'content_type': content_type,
        })(data)

    def test_post_valid_image(self):
        """Valid image returns success"""
        from django.test import RequestFactory
        factory = RequestFactory()
        fake_file = self._make_image()
        request = factory.post('/editorjs/image_upload/', {'image': fake_file})

        view = ImageUploadView()
        response = view.post(request)

        data = _json_response(response)
        assert data['success'] == 1
        assert 'file' in data

    def test_post_invalid_content_type(self):
        """Non-image content type is rejected"""
        from django.test import RequestFactory
        factory = RequestFactory()
        fake_file = self._make_image(content_type='text/plain', name='test.txt')
        request = factory.post('/editorjs/image_upload/', {'image': fake_file})

        view = ImageUploadView()
        response = view.post(request)

        data = _json_response(response)
        assert data['success'] == 0

    def test_post_no_file(self):
        """Missing file returns failure"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post('/editorjs/image_upload/', {})

        view = ImageUploadView()
        response = view.post(request)

        data = _json_response(response)
        assert data['success'] == 0


class TestImageByUrl:
    def test_post_with_url(self):
        """Valid URL returns success"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post(
            '/editorjs/image_by_url/',
            data='{"url": "https://example.com/img.png"}',
            content_type='application/json',
        )

        view = ImageByUrl()
        response = view.post(request)

        data = _json_response(response)
        assert data['success'] == 1
        assert data['file']['url'] == 'https://example.com/img.png'

    def test_post_without_url(self):
        """Missing url key returns failure"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post(
            '/editorjs/image_by_url/',
            data='{}',
            content_type='application/json',
        )

        view = ImageByUrl()
        response = view.post(request)

        data = _json_response(response)
        assert data['success'] == 0
