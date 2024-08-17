# test_scraper.py
from scraper import scrape_products

search_term = 'bulbo'
products = scrape_products(search_term)
print(products)
