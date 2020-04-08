
import re
import json
import tempfile

from superdesk.datalayer import SuperdeskJSONEncoder
from superdesk.io.feed_parsers import APMediaFeedParser

from cp.orangelogic import OrangelogicSearchProvider


class CP_APMediaFeedParser(APMediaFeedParser):

    def process_slugline(self, slugline):
        return re.sub(r'--+', '-', re.sub(r'[ !"#$%&()*+,./:;<=>?@[\]^_`{|}~\\]', '-', slugline))

    def parse(self, data, provider=None):
        item = super().parse(data, provider=provider)
        if item.get('slugline'):
            item['slugline'] = self.process_slugline(item['slugline'])

        with open('/tmp/{}.json'.format(item['slugline']), mode='wt') as f:
            json.dump(data, f, indent=2, default=SuperdeskJSONEncoder().default)
            print('saved', f.name)

        self.parse_associations(data, item)

        return item

    def parse_associations(self, data, item):
        try:
            assoc = data['data']['item']['associations']
        except KeyError:
            return

        item['associations'] = {}
        orange = OrangelogicSearchProvider({'config': {}})

        for key, val in assoc.items():
            guid = val['altids']['itemid']
            related = orange.fetch(guid)
            item['associations'][key] = related
