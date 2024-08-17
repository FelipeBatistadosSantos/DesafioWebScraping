import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_products(search_term):
    url = f"https://www.lojamaeto.com/busca?q={search_term}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for item in soup.select('.product-list .product-list-loading-images .template-01'):
        nome = item.select_one('.product-name').text.strip()
        preco_antigo = item.select_one('.old-price').text.strip() if item.select_one('.old-price') else None
        preco_pix = item.select_one('.price-boleto').text.strip() if item.select_one('.price-boleto') else None
        preco_cartao = item.select_one('.card-price').text.strip() if item.select_one('.card-price') else None
        img_url = item.select_one('.img-principal.lazyautosizes.ls-is-cached.lazyloaded img')['src'] if item.select_one('.img-principal.lazyautosizes.ls-is-cached.lazyloaded img') else None

        product = {
            'Nome': nome,
            'Preço Antigo': preco_antigo,
            'Preço Pix': preco_pix,
            'Preço Cartão': preco_cartao,
            'URL Imagem': img_url,
        }
        products.append(product)
    
    return products

def save_to_csv(products, filename='produtos.csv'):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False, encoding='utf-8')
