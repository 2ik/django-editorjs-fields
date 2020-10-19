import os

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .config import (EDITORJS_IMAGE_NAME, EDITORJS_IMAGE_NAME_ORIGINAL,
                     EDITORJS_IMAGE_NAME_POSTFIX, EDITORJS_IMAGE_UPLOAD_PATH)
from .utils import storage


class ImageUploadView(View):
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if 'image' in request.FILES:
            the_file = request.FILES['image']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png',
                'image/webp',
                'image/gif',
            ]
            if the_file.content_type not in allowed_types:
                return JsonResponse(
                    {'success': 0, 'message': 'You can only upload images.'}
                )

            # filesize = len(file['content'])
            # filetype = file['content-type']

            filename, extension = os.path.splitext(the_file.name)

            if EDITORJS_IMAGE_NAME_ORIGINAL:
                filename = filename + EDITORJS_IMAGE_NAME_POSTFIX
            else:
                filename = EDITORJS_IMAGE_NAME

            filename += extension

            path = storage.save(
                os.path.join(EDITORJS_IMAGE_UPLOAD_PATH, filename), the_file
            )
            link = storage.url(path)

            return JsonResponse({'success': 1, 'file': {"url": link}})
        return JsonResponse({'success': 0})
