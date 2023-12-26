from typer import Option, Typer
from typing import Optional

from scraper.command.services import ScraperCommandService

app: Typer = Typer()
services: ScraperCommandService = ScraperCommandService()

@app.command(name="scrape", help="Menjalankan Scraping semua halaman pada satu situs berdasarkan kata kunci tertentu")
def scrape(search_query: str, filepath: Optional[str] =  Option(None, help="Digunakan untuk Menentukan lokasi generate laporan hasil scraping, (Jika Diisi) contoh ./data.csv"), is_csv: Optional[bool] = Option(False, help="generate hasil scraping menjadi CSV, jika Filepath diisi"), is_excel: Optional[bool] = Option(False, help="generate hasil scraping menjadi file excel, (Jika Filepath diisi)"), is_json: Optional[bool]= Option(False, help="generate hasil scraping menjadi sebuah File JSON jika filepath diisi")):
    total_products = services.scrape(search_query=search_query, filepath=filepath, is_csv=is_csv, is_excel=is_excel, is_json=is_json)
    return total_products
    
@app.command(name="spesific_scrape", help="scraping situs berdasarkan kata kunci dan halaman tertentu")
def spesific_scrape(search_query: str, page: int,  filepath: Optional[str] =  Option(None, help="Digunakan untuk Menentukan lokasi generate laporan hasil scraping, (Jika Diisi) contoh ./data.csv"), is_csv: Optional[bool] = Option(False, help="generate hasil scraping menjadi CSV, jika Filepath diisi"), is_excel: Optional[bool] = Option(False, help="generate hasil scraping menjadi file excel, (Jika Filepath diisi)"), is_json: Optional[bool]= Option(False, help="generate hasil scraping menjadi sebuah File JSON jika filepath diisi")):
    products = services.spesific_scrape(search_query=search_query, page=page, filepath=filepath, is_csv=is_csv, is_excel=is_excel, is_json=is_json)
    return products