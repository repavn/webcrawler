import sys
from classes.content import ContentFetcher

fetcher = ContentFetcher(url=sys.argv[1])
fetcher.get_response()
htree = fetcher.get_html_tree()

catalog = htree.xpath("//header[contains(@class, 'MainLayout__header')]/"
                      "div[contains(@class, 'js--MainHeader__inner_bottom')]"
                      "/div[contains(@class, 'MainHeader__catalog-block')]/"
                      "div[contains(@class, 'MainHeader__catalog')]/a/@href")

print('catalog', catalog)
