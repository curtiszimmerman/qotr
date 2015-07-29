import json
from tornado import testing, httpserver

from qotr.server import make_application
from qotr.channels import Channels

class TestChannelHandler(testing.AsyncHTTPTestCase):
    '''
    Test the channel creation handler.
    '''

    port = None
    application = None

    def get_app(self):
        Channels.reset()
        return make_application()

    def test_create(self):
        salt = "common"
        channel_id = "test-channel"

        body = "&".join([
            "id={channel_id}",
            "salt={salt}",
            "key_hash=hmac-key"
        ]).format(**locals())

        response = json.loads(self.fetch(
            '/c/new', method='POST',
            body=body
        ).body.decode('utf8'))

        self.assertEqual({
            "salt": salt,
            "id": channel_id
        }, response)


    def test_confict(self):
        body = "&".join([
            "id=common",
            "salt=test-channel",
            "key_hash=hmac-key"
        ])

        self.fetch('/c/new', method='POST', body=body)
        response = json.loads(self.fetch(
            '/c/new', method='POST',
            body=body
        ).body.decode('utf8'))

        self.assertTrue("error" in response)
