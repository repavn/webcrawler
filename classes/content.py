import time
import pickle
from pprint import pprint

import redis
import requests
from collections import namedtuple
from io import StringIO
from lxml import etree

from utils.constants import DEFAULT_HEADERS, CACHE_TIME, REQUEST_ATTEMPTS, REQUEST_TIMEOUT, REQUEST_LATENCY
from utils.functions import get_first_or_none

ExtractXpathConfig = namedtuple('ExtractXpathConfig', [
    'index_url', 'catalog_link_xpath', 'categories_list_xpath',
    'deep_categories_xpath'
])
redis_connector = redis.Redis(host='localhost', port=6379)


class Validator(object):
    """validators of parameters - here"""
    pass

# TODO: watermark for images
# TODO: normalize logs


class ContentFetcher(object):
    """
        Download and formalize content (for data extracting in the future)
    """
    url = None
    response = None

    # TODO: randomize user-agent choice
    default_headers = DEFAULT_HEADERS
    headers = None

    def __init__(self, url: str, headers: dict = None):
        # TODO: validate url
        self.url = url
        if 'https:' not in url and 'http:' not in url:
            self.url = f'https://{url}/'
        if headers:
            self.headers = {**self.default_headers, **headers}
        else:
            self.headers = self.default_headers

    def _force_get_response(self, url):
        time.sleep(REQUEST_LATENCY)
        for attempt in range(1, REQUEST_ATTEMPTS + 1):
            status_code = None
            try:
                resp = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
                status_code = resp.status_code
                print(f"{url} {status_code}")
                resp.raise_for_status()
                return resp
            except Exception as e:
                print(f"{url} _force_get_response error: {str(e)}")
                if status_code and status_code in (429, 443):
                    time.sleep(REQUEST_LATENCY)

    def get_response(self, use_cache=True):
        # TODO: m.b hash key? add post data to key, headers...
        if use_cache:
            serialized_resp = redis_connector.get(self.url)
            cached_response = pickle.loads(redis_connector.get(self.url)) if serialized_resp else None
            if not cached_response:
                http_response = self._force_get_response(self.url)
                response = pickle.dumps(http_response)
                redis_connector.set(self.url, response, ex=CACHE_TIME)
                cached_response = pickle.loads(redis_connector.get(self.url))
            self.response = cached_response
        else:
            self.response = requests.get(self.url, headers=self.default_headers)
            self.response.raise_for_status()

    def convert_to_html_etree(self):
        if not self.response:
            return None
        parser = etree.HTMLParser()
        try:
            html_etree = etree.parse(StringIO(self.response.text), parser)
        except Exception as e:
            print(f" {str(e)}")
            html_etree = None
        return html_etree


class DataExtractor(object):
    """
        Extract data from existing content
    """
    config = None
    root_page = None
    catalog_page = None
    category_tree = None

    def __init__(self, config: ExtractXpathConfig):
        self.config = config

    def _get_content_from_url(self, url: str) -> etree._ElementTree:
        fetcher = ContentFetcher(url=url)
        fetcher.get_response()
        html_tree_res = fetcher.convert_to_html_etree()
        return html_tree_res

    def _get_root_page(self):
        self.root_page = self._get_content_from_url(self.config.index_url)

    def _extract_catalog(self):
        # here - we init category tree
        self._get_root_page()
        catalog_link = get_first_or_none(
            self.root_page.xpath(self.config.catalog_link_xpath)
        )
        self.catalog_page = self._get_content_from_url(catalog_link)
        # TODO: extract category name
        self.category_tree = {
            'url': catalog_link,
            'children': []
        }

    def _extract_root_categs(self):
        self._extract_catalog()
        category_links = self.catalog_page.xpath(self.config.categories_list_xpath)
        if isinstance(category_links, str):
            category_links = [category_links]
        for category_link in category_links:
            # category_page = self._get_content_from_url(category_link)
            self.category_tree['children'].append(
                {'url': category_link, 'children': []}
            )

    def _deep_extract_categs(self, parent):
        parent_page = self._get_content_from_url(parent['url'])
        if parent_page is None:
            return
        urls = parent_page.xpath(self.config.deep_categories_xpath)
        if not urls:
            return
        parent['children'] = urls
        for url in urls:
            child = {'url': url, 'children': []}
            self._deep_extract_categs(child)

    def get_category_tree(self):
        self._extract_root_categs()
        for root_child in self.category_tree['children']:
            self._deep_extract_categs(root_child)
            pprint(root_child)
