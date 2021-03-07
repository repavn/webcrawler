from lxml import etree
import requests

class Validators(object):
    """validators of parameters - here"""
    pass


class ContentFetcher(object):
    """Just getting data"""
    url = None
    html_tree = None
    response = None

    # TODO: randomize user-agent choice
    default_headers = {
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
    }

    def __init__(self, url):
        # TODO: validate url
        self.url = url
    
    def get_response():
        response = requests.get(self.url, headers=self.default_headers)


    def get_html_tree():
        # self.html_tree
        pass
