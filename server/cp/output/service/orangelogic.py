
from flask import current_app as app, json

from superdesk.utc import utcnow
from superdesk.publish import register_transmitter
from superdesk.publish.publish_service import PublishService
from superdesk.media.media_operations import guess_media_extension

from cp.orangelogic import OrangelogicSearchProvider

UPLOAD_MEDIA_API = '/API/UploadMedia/v3.0/UploadNewMedia'
FOLDERS_READ_API = '/API/DataTable/V2.2/Documents.Folder.Upload-Folder:Read'
FOLDERS_CREATE_API = '/API/DataTable/V2.2/Documents.Folder.Upload-Folder:Create'


class OrangelogicManager(OrangelogicSearchProvider):

    FOLDER = 'CREATE_TEST'
    PARENT_FOLDER = 'SUPERDESK'

    def get_folder_id(self, name):
        params = {'CoreField.Title': name}
        resp = self._auth_request(FOLDERS_READ_API, params=params)
        return resp.json()['Response'][0]['RecordID']

    def create_folder(self, name):
        parent = self.get_folder_id(self.PARENT_FOLDER)
        assert parent, 'parent folder not found'
        data = {
            'CoreField.Title': name,
            'CoreField.Parent-folder': parent,
        }
        api = '{}?{}'.format(FOLDERS_CREATE_API, '&'.join([
            '{key}:={val}'.format(key=key, val=val)
            for key, val in data.items()
        ]))
        resp = self._auth_request(api)
        return resp.json()['Response']['RecordID']

    def get_upload_folder_name(self):
        """TODO: make it dynamic based on year/month"""
        return self.FOLDER

    def upload_folder(self):
        name = self.get_upload_folder_name()
        existing = self.get_folder_id(name)
        if existing:
            return existing
        return self.create_folder(name)

    def upload(self, binary, filename):
        data = {
            'FileName': filename,
            'InputStream': binary.read(),
            'FolderRecordID': self.upload_folder(),
            'UploadMode': 'ProcessInLine',
        }

        resp = self._auth_request(UPLOAD_MEDIA_API, data=data, method='POST', retry=0)
        print('upload', resp.json())


class Orangelogic(PublishService):

    NAME = 'Orangelogic'

    def _transmit(self, queue_item, subscriber):
        ol = OrangelogicManager({
            'config': {
                'username': app.config['ORANGELOGIC_USERNAME'],
                'password': app.config['ORANGELOGIC_PASSWORD'],
            }
        })

        item = json.loads(queue_item['formatted_item'])

        try:
            rendition = item['renditions']['original']
        except KeyError:
            return

        media = app.media.get(rendition['media'])
        filename = '{}{}'.format(item['guid'], guess_media_extension(item['mimetype']))
        ol.upload(media, filename)

    
def init_app(_app):
    register_transmitter('orangelogic', Orangelogic(), {})
