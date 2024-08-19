import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from unidecode import unidecode
import re

def scrape_products(search_term, page_number=1):
    url = f"https://www.lojamaeto.com/busca?q={search_term}&p={page_number}" if page_number > 1 else f"https://www.lojamaeto.com/busca?q={search_term}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.select('.product-one-of-three, .product-two-of-three, .product-three-of-three'):
            nome = item.select_one('.product-name').text.strip()
            preco_antigo = item.select_one('.old-price').text.strip() if item.select_one('.old-price') else None
            preco_pix = item.select_one('.price-boleto').text.strip() if item.select_one('.price-boleto') else None
            preco_cartao = extract_preco_cartao(item)
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

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

def scrape_all_pages(search_term):
    page_number = 1
    all_products = []

    while True:
        print(f"Coletando dados da página {page_number}...")
        products = scrape_products(search_term, page_number)
        
        if not products:
            print(f"Nenhum produto encontrado na página {page_number}. Finalizando a coleta.")
            break  # Se não houver produtos, pare a coleta
        
        all_products.extend(products)
        
        # Verifica se há uma próxima página
        next_page_url = f"https://www.lojamaeto.com/busca?q={search_term}&p={page_number + 1}"
        try:
            response = requests.get(next_page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verifica se há produtos na próxima página
            if not soup.select('.product-one-of-three, .product-two-of-three, .product-three-of-three'):
                print(f"Próxima página não encontrada. Finalizando a coleta.")
                break

        except requests.exceptions.RequestException as e:
            print(f"Erro ao verificar a próxima página: {e}")
            break

        page_number += 1

    return all_products

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
    df['Preço Cartão'] = df['Preço Cartão']

    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    if not os.path.exists(master_csv_path):
        df.to_csv(master_csv_path, mode='w', header=True, index=False, encoding='utf-8')
    else:
        df.to_csv(master_csv_path, mode='a', header=False, index=False, encoding='utf-8')

    return csv_path

def main(search_term, search_count):
    products = scrape_all_pages(search_term)
    save_to_csv(products, search_term, search_count)
    print(f"Dados salvos em 'data/{search_term.replace(' ', '-').lower()}{search_count}.csv' e 'data/todos_produtos.csv'.")

search_term = "lampada"
search_count = 1
main(search_term, search_count)
