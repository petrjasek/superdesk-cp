
import os
import flask
import unittest


from cp.output.service.orangelogic import Orangelogic


class OrangelogicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flask.Flask(__name__)
        self.app.config.update({
            'ORANGELOGIC_USERNAME': os.environ.get('ORANGELOGIC_USERNAME'),
            'ORANGELOGIC_PASSWORD': os.environ.get('ORANGELOGIC_PASSWORD'),
        })

    def test_transmit(self):
        service = Orangelogic()
        item = {}
        subscriber = {}
        with self.app.app_context():
            service._transmit(item, subscriber)
        self.assertTrue(False)
