from django_editorjs_fields.utils import get_default_storage, get_hostname_from_url


class TestGetHostnameFromUrl:
    def test_https_url(self):
        assert get_hostname_from_url('https://www.youtube.com/watch?v=test') == 'www.youtube.com'

    def test_http_url(self):
        assert get_hostname_from_url('http://example.com/path') == 'example.com'

    def test_url_with_port(self):
        assert get_hostname_from_url('https://localhost:8000/media/img.png') == 'localhost'

    def test_subdomain(self):
        assert get_hostname_from_url('https://player.vimeo.com/video/123') == 'player.vimeo.com'


class TestGetDefaultStorage:
    def test_returns_storage(self):
        """get_default_storage returns a storage instance"""
        storage = get_default_storage()
        assert storage is not None
        # Should have standard storage methods
        assert hasattr(storage, 'save')
        assert hasattr(storage, 'url')
