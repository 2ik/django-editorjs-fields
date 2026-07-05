import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.mark.django_db
class TestUrls:
    def test_image_upload_url(self):
        from django.urls import reverse
        url = reverse('editorjs_image_upload')
        assert url == '/image_upload/'

    def test_linktool_url(self):
        from django.urls import reverse
        url = reverse('editorjs_linktool')
        assert url == '/linktool/'

    def test_image_by_url_url(self):
        from django.urls import reverse
        url = reverse('editorjs_image_by_url')
        assert url == '/image_by_url/'

    def test_image_by_url_no_auth(self):
        """ImageByUrl does NOT require authentication"""
        client = Client()
        response = client.post(
            '/image_by_url/',
            data='{}',
            content_type='application/json',
        )
        assert response.status_code == 200

    def test_image_upload_staff_access(self):
        """Staff user can access image upload"""
        client = Client()
        user = User.objects.create_user(username='test', password='pass', is_staff=True)
        client.force_login(user)
        response = client.post('/image_upload/')
        assert response.status_code == 200

    def test_linktool_staff_access(self):
        """Staff user can access linktool"""
        client = Client()
        user = User.objects.create_user(username='test', password='pass', is_staff=True)
        client.force_login(user)
        response = client.get('/linktool/')
        assert response.status_code == 200
