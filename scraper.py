import requests
from bs4 import BeautifulSoup
import json

def scrape_products(search_term):
    url = f"https://www.lojamaeto.com/busca?q={search_term}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for item in soup.select('.product-list .product-item'):
        nome = item.select_one('.product-name').text.strip()
        preco_antigo = item.select_one('.old-price').text.strip() if item.select_one('.old-price') else None
        preco_pix = item.select_one('.price-boleto').text.strip() if item.select_one('.price-boleto') else None
        preco_cartao = item.select_one('.card-price').text.strip() if item.select_one('.card-price') else None
        img_url = item.select_one('img')['src'] if item.select_one('img') else None

        product = {
            'Nome': nome,
            'Preço Antigo': preco_antigo,
            'Preço Pix': preco_pix,
            'Preço Cartão': preco_cartao,
            'URL Imagem': img_url,
        }
        products.append(product)
        print(f"Nome: {nome}, Preço Pix: {preco_pix}, Preço Cartão: {preco_cartao}, Imagem: {img_url}")

    
    return products

def extract_product_details(product_url):
    # Função para coletar características detalhadas da página do produto
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    characteristics = {}

    # Exemplo de extração
    for characteristic in soup.select('.characteristics li'):
        key = characteristic.select_one('.key').text.strip()
        value = characteristic.select_one('.value').text.strip()
        characteristics[key] = value
    
    return characteristics

