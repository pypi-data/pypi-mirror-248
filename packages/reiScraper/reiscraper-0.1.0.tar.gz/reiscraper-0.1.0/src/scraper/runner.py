from typing import Optional, Any
from rich import print

from scraper.rei import ReiSpider

class Runner(object):
    def __init__(self) -> None:
        self.spider : Optional[ReiSpider] = ReiSpider()

    def generate_product(self, search_query: str, page: Optional[int]=None) -> list[dict[str, Any]]:
        #untuk mendapatkan html
        if page != None:
            soup = self.spider.search_product(search_query=search_query, page_number=page)
            products: list[dict[str, Any]] = self.spider.get_product_list(soup=soup)
            return products
        else:
            soup = self.spider.search_product(search_query=search_query)
            products: list[dict[str, Any]] = self.spider.get_product_list(soup=soup)
            return products
        
    def generate_all_products(self, search_query: str) -> list[dict[str, Any]]:
        
        total_products: list[dict[str, Any]] = []
        search = self.spider.search_product(search_query=search_query)
        pages = self.spider.get_page_number(soup=search)
        for page in range(1, pages):
            print("Scraping Page", page)
            products = self.generate_product(search_query=search_query, page=page)
            total_products += products
        
        return total_products   