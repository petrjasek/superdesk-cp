
from flask import current_app as app

from superdesk.utc import utcnow
from superdesk.publish import register_transmitter
from superdesk.publish.publish_service import PublishService

from cp.orangelogic import OrangelogicSearchProvider

FOLDERS_READ_API = '/API/DataTable/V2.2/Documents.Folder.Default:Read'


class Orangelogic(PublishService):

    NAME = 'Orangelogic'

    def _transmit(self, queue_item, subscriber):
        ol = OrangelogicSearchProvider({
            'config': {
                'username': app.config['ORANGELOGIC_USERNAME'],
                'password': app.config['ORANGELOGIC_PASSWORD'],
            }
        })

        folder = self._setup_folder(ol)

        item = json.loads(queue_item['formatted_item'])

        try:
            rendition = item['renditions']['original']
        except KeyError:
            pass
         
        return

    def _setup_folder(self, ol):
        now = utcnow()
        folder_name = 'superdesk'
        params = {'CoreField.Identifier': folder_name}
        resp = ol._auth_request(FOLDERS_READ_API, **params)
        print('resp', resp)



def init_app(_app):
    register_transmitter('orangelogic', Orangelogic(), {})