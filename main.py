import pprint
import sys
from classes.content import ExtractXpathConfig, DataExtractor


# TODO: docker... (wrap into ubuntu image, install python, system libs etc.)
# TODO: async run...


config = ExtractXpathConfig(
    index_url=sys.argv[1],
    catalog_link_xpath="//header[contains(@class, 'MainLayout__header')]"
                       "/div[contains(@class, 'js--MainHeader__inner_bottom')]"
                       "/div[contains(@class, 'MainHeader__catalog-block')]"
                       "/div[contains(@class, 'MainHeader__catalog')]/a/@href",
    categories_list_xpath="//a[contains(@class, 'CatalogLayout__link_level-1')]/@href",
    deep_categories_xpath="//a[contains(@class, 'CatalogCategoryCard__link')]/@href"
)

data_extractor = DataExtractor(config)
data_extractor.get_category_tree()

print("category tree:\n")
pprint.pprint(data_extractor.category_tree)
