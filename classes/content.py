from io import StringIO
from lxml import etree
import requests

from utils.constants import DEFAULT_HEADERS


class Validators(object):
    """validators of parameters - here"""
    pass

# TODO: watermark for images
# TODO: normalize logs


class ContentFetcher(object):
    url = None
    response = None

    # TODO: randomize user-agent choice
    default_headers = DEFAULT_HEADERS

    def __init__(self, url, headers=None):
        # TODO: validate url
        self.url = f'https://{url}/'

    def get_response(self):
        self.response = requests.get(self.url, headers=self.default_headers)
        self.response.raise_for_status()
        print('response', self.response.status_code)

    def get_html_tree(self):
        parser = etree.HTMLParser()
        html_tree = etree.parse(StringIO(self.response.text), parser)
        print('self.html_tree', html_tree)
        return html_tree
