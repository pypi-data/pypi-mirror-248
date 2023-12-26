import httpx #libary yang digunakan untuk mengoneksikan http
import json

from typing import Any, Optional #dari modul typing mengimport typedata Any --> semua jenis type data
from selectolax.parser import HTMLParser
from rich import print #supaya ketika print ada warnanya
from scraper.utils.validation import Validation

class ReiSpider(object):
    def __init__(self, validation: Validation = Validation()):
        self.validation: Validation = validation
        self.base_url: str = "https://www.rei.com"

    def search_product(self, search_query: str, page_number: Optional[int]=None) -> HTMLParser:
        if page_number == None or page_number == 1:
            url:str = self.base_url + "/search?q={}".format(search_query)
        else:
            url:str = self.base_url + "/search?q={}&page={}".format(search_query,page_number)

        headers: dict[str, Any] = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

        response = httpx.get(url=url, headers=headers)

        f = open("search_response.html", "w+", encoding="UTF-8")
        f.write(response.text)
        f.close()

        soup: HTMLParser = HTMLParser(response.text)

        return soup
    
    def get_page_number (self, soup = HTMLParser) -> int:
        pages = soup.css_first('a[data-id="pagination-test-link"]').text()
        return self.validation.is_valid_pages_number(pages)

        

    def get_product_detail(self, soup:HTMLParser):
        # data mentah
        scripts = soup.css_first("script#modelData")

        # teknik parsing
        datas = self.get_data_from_json(scripts.text())
        return datas

    def get_data_from_json(self, obj:str) -> dict[str, Any]:
        data_dict : dict[str, any] = {}
        datas = json.loads(obj)
        
    
        #proses scrapping json
        product = datas["pageData"]["product"]
        product_price = product["availablePrices"]
        product_url = self.base_url + product ["canonicalUrl"]
        product_review = product["reviewSummary"]
        product_size = product["sizes"]
        product_size_chart = product["sizeChart"]
        product_image = product["images"]
        product_specs = product["techSpecs"]
        product_feature = product["features"] 
        product_sku = product["skus"]
        product_color = product["colors"]

        phone_number = datas["openGraphProperties"]["og:phone_number"]
        phone_number = datas["contactPhoneNumber"] 

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
        data_dict["product_sku"] = product_sku
        data_dict["product_color"] = product_color
    
        return data_dict
    
    def get_product_items(self, soup:HTMLParser) -> list[str]:
        urls: list[str] = []
        search_items = soup.css_first("div#search-results")
        products = search_items.css("ul.cdr-grid_13-5-2 > li")
        for product in products:
            product_url = product.css_first("a").attributes.get("href")
            urls.append(self.base_url + product_url)

        #cetak url yang ditemukan
        print("Total product URL's found: {}".format(len(urls)))
        return urls
    
    def get_product_list (self, soup: HTMLParser) -> list[str]:
        products : list[dict[str, Any]] = []

        products_list = self.get_product_items(soup=soup)
        for index, product in enumerate(products_list, start=1):
            print("generate product data on URL: {} ({} of {})".format(product, index, len(products_list)))
            product_data = self.get_product_data(url=product)
            products.append(product_data)

        #proses product disini
        return product
    
    def get_product_data (self, url: str) -> dict[str, Any]:
        headers: dict[str, Any] = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

        #olah response
        response = httpx.get(url=url, headers=headers)

        f = open("response_detail.html", "w+", encoding="UTF-8")
        f.write(response.text)
        f.close()

        soup: HTMLParser = HTMLParser(response.text)
        
        #data ambil disini
        product = self.get_product_detail(soup=soup)
        
        #hasilnya dikembalikan
        return product



        #scraping proses
        #data mentah

