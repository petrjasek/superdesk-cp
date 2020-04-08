
import json
import flask
import unittest

from unittest.mock import MagicMock
from tests.ingest.parser import get_fixture_path

from cp.ingest import CP_APMediaFeedParser


with open(get_fixture_path('item.json', 'ap')) as fp:
    data = json.load(fp)


class CP_AP_ParseTestCase(unittest.TestCase):

    app = flask.Flask(__name__)

    def test_slugline(self):
        parser = CP_APMediaFeedParser()
        self.assertEqual('foo-bar-baz', parser.process_slugline('foo bar/baz'))
        self.assertEqual('foo-bar', parser.process_slugline('foo-bar'))
        self.assertEqual('foo-bar', parser.process_slugline('foo - bar'))

    def test_parse_associations(self):
        parser = CP_APMediaFeedParser()
        item = {}
        with self.app.app_context():
            parser.parse_associations(data, item)
        self.assertIn('associations', item)
