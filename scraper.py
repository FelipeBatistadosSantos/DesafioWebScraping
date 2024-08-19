import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from unidecode import unidecode
import re

def scrape_products(search_term):
    url = f"https://www.lojamaeto.com/busca?q={search_term}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []
    for item in soup.select('.product-one-of-three, .product-two-of-three, .product-three-of-three'):
        nome = item.select_one('.product-name').text.strip()
        preco_antigo = item.select_one('.old-price').text.strip() if item.select_one('.old-price') else None
        preco_pix = item.select_one('.price-boleto').text.strip() if item.select_one('.price-boleto') else None
        preco_cartao = extract_preco_cartao(item)  # Use the updated function to get 'Preço Cartão'
        img_url = item.select_one('.img-principal')['data-src'] if item.select_one('.img-principal') else None

        product = {
            'Nome': nome,
            'Preço Antigo': preco_antigo,
            'Preço Pix': preco_pix,
            'Preço Cartão': preco_cartao,
            'URL Imagem': img_url,
        }
        products.append(product)
    
    return products

def clean_product_name(nome):
    nome_sem_acentos = unidecode(nome)
    nome_sem_acentos_e_aspas = nome_sem_acentos.replace('"', '')
    return nome_sem_acentos_e_aspas.strip()

def remove_currency_symbol(value):
    if isinstance(value, str):
        value = value.replace('R$', '').replace(',', '.').strip()
    elif value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None

def extract_preco_cartao(item):
    type_payment_condiction = item.select_one('.type-payment-condiction')
    if type_payment_condiction:
        parcelas = type_payment_condiction.text.strip()
        match = re.search(r'(\d+)X de\s+R\$\s*(\d+,\d+)', parcelas)
        if match:
            number_of_installments = match.group(1)
            installment_value = match.group(2)
            return f"{number_of_installments}X de R${installment_value}"
    return None

def save_to_csv(products, search_term, search_count):
    clean_term = search_term.replace(' ', '-').lower()
    filename = f"{clean_term}{search_count}.csv"
    csv_path = os.path.join('data', filename)
    master_csv_path = os.path.join('data', 'todos_produtos.csv')
    
    column_titles = ['Nome', 'Preço Antigo', 'Preço Pix', 'Preço Cartão', 'URL Imagem']
    df = pd.DataFrame(products, columns=column_titles)

    df['Nome'] = df['Nome'].apply(clean_product_name)
    df['Preço Antigo'] = df['Preço Antigo'].apply(remove_currency_symbol)
    df['Preço Pix'] = df['Preço Pix'].apply(remove_currency_symbol)
    df['Preço Cartão'] = df['Preço Cartão']  # Already formatted by extract_preco_cartao

    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    if not os.path.exists(master_csv_path):
        df.to_csv(master_csv_path, mode='w', header=True, index=False, encoding='utf-8')
    else:
        df.to_csv(master_csv_path, mode='a', header=False, index=False, encoding='utf-8')

    return csv_path

def extract_characteristics(soup):
    characteristics = {}

    flex_divs = soup.select('div.flex')
    
    for flex_div in flex_divs:
        dt_elements = flex_div.find_all('dt')
        dd_elements = flex_div.find_all('dd')
        
        for dt, dd in zip(dt_elements, dd_elements):
            title = dt.get_text(strip=True)
            description = dd.get_text(strip=True)
            
            characteristics[title] = description
    
    return json.dumps(characteristics, ensure_ascii=False, indent=4)

def extract_product_characteristics(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    characteristics = {}
    
    for flex_div in soup.select('div.flex'):
        dt_elements = flex_div.find_all('dt')
        dd_elements = flex_div.find_all('dd')

        for dt, dd in zip(dt_elements, dd_elements):
            title = dt.get_text(strip=True)
            description = dd.get_text(strip=True)
            characteristics[title] = description

    return characteristics

def scrape_products_and_characteristics(search_term):
    url = f"https://www.lojamaeto.com/busca?q={search_term}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_products_data = []
    for item in soup.select('.product-one-of-three, .product-two-of-three, .product-three-of-three'):
        product_url = item.select_one('a')['href']  # Obter a URL do produto
        product_page_url = f"https://www.lojamaeto.com{product_url}"

        try:
            characteristics = extract_product_characteristics(product_page_url)
            all_products_data.append(characteristics)
        except Exception as e:
            print(f"Erro ao extrair características para {product_page_url}: {e}")

    with open('produtos.json', 'w') as f:
        json.dump(all_products_data, f, indent=4)

def check_data():
    df = pd.read_csv('data/todos_produtos.csv')
    print(df.dtypes)
    print(df.head())

def main(search_term, search_count):
    products = scrape_products(search_term)
    save_to_csv(products, search_term, search_count)
    check_data()

search_term = "lampada"
search_count = 1
main(search_term, search_count)
