import io
import os
import flask
import unittest
import superdesk

from flask import json
from tests.mock import resources, media_storage
from unittest.mock import patch
from httmock import urlmatch, HTTMock

from cp.output.service.orangelogic import Orangelogic

from tests.orangelogic_test import auth_ok, fixture, read_fixture


@urlmatch(netloc=r'example\.com$', path=r'/API/DataTable/V2.2/Documents.Folder.Upload-Folder:Read')
def data_folder_read_ok(url, request):
    return read_fixture('orangelogic_data_folder_read_ok.json')


@urlmatch(netloc=r'example\.com$', path=r'/API/UploadMedia/v3.0/UploadNewMedia', method='POST')
def upload_media_ok(url, request):
    return read_fixture('orangelogic_upload_ok.json')


class OrangelogicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flask.Flask(__name__)
        self.app.media = media_storage
        self.app.config.update({
            'ORANGELOGIC_URL': 'https://example.com/',
            'ORANGELOGIC_USERNAME': os.environ.get('ORANGELOGIC_USERNAME'),
            'ORANGELOGIC_PASSWORD': os.environ.get('ORANGELOGIC_PASSWORD'),
        })

    def test_transmit(self):
        service = Orangelogic()
        item = {
            'guid': 'foo-bar',
            'mimetype': 'image/jpeg',
            'renditions': {
                'original': {
                    'media': 'foo',
                }
            }
        }

        subscriber = {}
        queue_item = {
            'formatted_item': json.dumps(item),
        }

        with open(fixture('9e627f74b97841b3b8562b6547ada9c7-d1538139479c43e88021152.jpg'), 'rb') as img:
            self.app.media.get.return_value = io.BytesIO(img.read())

        with self.app.app_context():
            with patch.dict(superdesk.resources, resources):
                with HTTMock(auth_ok, data_folder_read_ok, upload_media_ok):
                    service._transmit(queue_item, subscriber)

        self.assertTrue(False)
