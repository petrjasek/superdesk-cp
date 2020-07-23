
from flask import current_app as app, json

from superdesk.utc import utcnow
from superdesk.publish import register_transmitter
from superdesk.publish.publish_service import PublishService

from cp.orangelogic import OrangelogicSearchProvider

FOLDERS_DEFAULT_READ_API = '/API/DataTable/V2.2/Documents.Folder.Default:Read'


class OrangelogicManager(OrangelogicSearchProvider):

    def setup_folder(self, name):
        params = {'CoreField.Title': name, 'format': 'json'}
        resp = ol._auth_request(FOLDERS_READ_API, **params)
        print('resp', resp)


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
        self._upload(ol, media)

    def _upload(self, ol, binary):

        folder_id = self._setup_folder(ol)

        
         params = {
             'FolderRecordId': folder_id,
             'FileName': 
         }

        return


def init_app(_app):
    register_transmitter('orangelogic', Orangelogic(), {})