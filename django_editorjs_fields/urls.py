from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from .views import ImageByUrl, ImageUploadView, LinkToolView

urlpatterns = [
    path(
        'image_upload/',
        staff_member_required(ImageUploadView.as_view()),
        name='editorjs_image_upload',
    ),
    path(
        'linktool/',
        staff_member_required(LinkToolView.as_view()),
        name='editorjs_linktool',
    ),
    path(
        'image_by_url/',
        ImageByUrl.as_view(),
        name='editorjs_image_by_url',
    ),
]
