import json
import logging
import os
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .config import (IMAGE_NAME, IMAGE_NAME_ORIGINAL, IMAGE_UPLOAD_PATH,
                     IMAGE_UPLOAD_PATH_DATE)
from .utils import storage

LOGGER = logging.getLogger('django_editorjs_fields')


class ImageUploadView(View):
    http_method_names = ["post"]
    # http_method_names = ["post", "delete"]

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

            filename, extension = os.path.splitext(the_file.name)

            if IMAGE_NAME_ORIGINAL is False:
                filename = IMAGE_NAME(filename=filename, file=the_file)

            filename += extension

            upload_path = IMAGE_UPLOAD_PATH

            if IMAGE_UPLOAD_PATH_DATE:
                upload_path += datetime.now().strftime(IMAGE_UPLOAD_PATH_DATE)

            path = storage.save(
                os.path.join(upload_path, filename), the_file
            )
            link = storage.url(path)

            return JsonResponse({'success': 1, 'file': {"url": link}})
        return JsonResponse({'success': 0})

    # def delete(self, request):
    #     path_file = request.GET.get('pathFile')

    #     if not path_file:
    #         return JsonResponse({'success': 0, 'message': 'Parameter "pathFile" Not Found'})

    #     base_dir = getattr(settings, "BASE_DIR", '')
    #     path_file = f'{base_dir}{path_file}'

    #     if not os.path.isfile(path_file):
    #         return JsonResponse({'success': 0, 'message': 'File Not Found'})

    #     os.remove(path_file)

    #     return JsonResponse({'success': 1})


class LinkToolView(View):
    http_method_names = ["get"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        url = request.GET.get('url', '')

        LOGGER.debug('Starting to get meta for: %s', url)

        if not any([url.startswith(s) for s in ('http://', 'https://')]):
            LOGGER.debug('Adding the http protocol to the link: %s', url)
            url = 'http://' + url

        validate = URLValidator(schemes=['http', 'https'])

        try:
            validate(url)
        except ValidationError as e:
            LOGGER.error(e)
        else:
            try:
                LOGGER.debug('Let\'s try to get meta from: %s', url)

                full_url = 'https://api.microlink.io/?' + \
                    urlencode({'url': url})

                req = Request(full_url, headers={
                    'User-Agent': request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
                })
                res = urlopen(req)
            except HTTPError as e:
                LOGGER.error('The server couldn\'t fulfill the request.')
                LOGGER.error('Error code: %s %s', e.code, e.msg)
            except URLError as e:
                LOGGER.error('We failed to reach a server. url: %s', url)
                LOGGER.error('Reason: %s', e.reason)
            else:
                res_body = res.read()
                res_json = json.loads(res_body.decode("utf-8"))

                if 'success' in res_json.get('status'):
                    data = res_json.get('data')

                    if data:
                        LOGGER.debug('Response meta: %s', data)
                        meta = {}
                        meta['title'] = data.get('title')
                        meta['description'] = data.get('description')
                        meta['image'] = data.get('image')

                        return JsonResponse({
                            'success': 1,
                            'link': data.get('url', url),
                            'meta': meta
                        })

        return JsonResponse({'success': 0})


class ImageByUrl(View):
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        body = json.loads(request.body.decode())
        if 'url' in body:
            return JsonResponse({'success': 1, 'file': {"url": body['url']}})
        return JsonResponse({'success': 0})
