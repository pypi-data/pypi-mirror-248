import json

from rich import print
from selectolax.parser import HTMLParser
from typing import Any

from scraper.utils.validation import Validation

class ReiSpiderDebug(object):
    def __init__(self, validation: Validation = Validation()):
        self.validation: Validation = validation
        self.base_url: str = "https://www.rei.com"

    def get_product_detail(self, soup: HTMLParser) -> dict[str, Any]:
        #data mentah
        scripts = soup.css_first("script#modelData")
        
        #teknik parsing
        datas = self.get_data_from_json(scripts.text())
        return datas
    
    def get_product_items(self, soup: HTMLParser) -> list[str]:
        urls: list[str] = []
        search_items = soup.css_first("div#search-result")
        products = search_items.css("ul.cdr-grid_13-5-2 > li")
        for product in products:
            product_url = product.css_first("a").attributes.get("href")
            urls.append(self.base_url + product_url)
        print(products)
        print("Total Product's URL's Found: {}".format(len(urls)))
    
    def get_data_from_json(self, obj:str) -> dict[str, Any]:
        data_dict : dict[str, any] = {}
        datas = json.loads(obj)
        
    
        #proses scrapping json
        product = datas["pageData"]["product"]
        product_price = product["availablePrices"]
        product_url = self.base_url + "/" + datas["canonical"]
        product_review = product["reviewSummary"]
        product_size = product["sizes"]
        product_size_chart = product["sizeChart"]
        product_image = product["images"]
        product_specs = product["techSpecs"]
        product_feature = product["features"]
        product_rating = product_review["ratingHistogram"]
        #product_rating = product["reviewSummary"]["ratingHistogram"] #ditanyakan
        product_sku = product["skus"]
        product_color = product["colors"]

        phone_number = datas["openGraphProperties"]["og:phone_number"]
        #phone_number = datas["contactPhoneNumber"] #ditanyakan

        #untuk menambahkan data
        data_dict["title"] = datas["title"]
        data_dict["phone_number"] = self.validation.is_valid_phone(phone_number)
        data_dict["product_price"] = product_price
        data_dict["product_url"] = product_url
        data_dict["product_review"] = product_review
        data_dict["product_size"] = product_size
        data_dict["product_size_chart"] = product_size_chart
        data_dict["product_image"] = product_image
        data_dict["product_specification"] = product_specs
        data_dict["product_feature"] = product_feature
        data_dict["product_rating"] = product_rating
        data_dict["product_sku"] = product_sku
        data_dict["product_color"] = product_color
    
        return data_dict