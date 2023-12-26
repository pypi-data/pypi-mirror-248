from typing import Any, Optional

from scraper.runner import Runner
from scraper.extractor import Extract

class ScraperCommandService(object):
    def __init__(self) -> None:
        self.runner : Runner = Runner()
        self.extract : Extract = Extract()

    def scrape(self, search_query: str, filepath: Optional[str]=None, is_csv: Optional[bool]=False, is_excel: Optional[bool]=False, is_json: Optional[bool]=False):
        total_products: list[dict[str, Any]] = self.runner.generate_all_products(search_query=search_query)

        if filepath != None:
            if is_csv:
                self.extract.to_csv(data=total_products, filepath=filepath)
            elif is_excel:
                self.extract.to_excel(data=total_products, filepath=filepath)
            elif is_json:
                self.extract.to_json(data=total_products, filepath=filepath)
            
            return total_products
        else:
            return total_products 
    
    def spesific_scrape(self, search_query: str, page: Optional[int]=None, filepath: Optional[str]=None, is_csv: Optional[bool]=False, is_excel: Optional[bool]=False, is_json: Optional[bool]=False):
        products: list[dict[str, Any]] = self.runner.generate_product(search_query=search_query, page=page)
        if filepath != None:
            if is_csv:
                self.extract.to_csv(data=products, filepath=filepath)
            elif is_excel:
                self.extract.to_excel(data=products, filepath=filepath)
            elif is_json:
                self.extract.to_json(data=products, filepath=filepath)
            
            return products
        else:
            return products 