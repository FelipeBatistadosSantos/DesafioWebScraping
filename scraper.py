import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

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
        preco_cartao = item.select_one('.price-cartao').text.strip() if item.select_one('.price-cartao') else None
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

def save_to_csv(products, filename='produtos.csv'):
    column_titles = ['Nome', 'Preço Antigo', 'Preço Pix', 'Preço Cartão', 'URL Imagem']
    df = pd.DataFrame(products, columns=column_titles)
    df.to_csv(filename, index=False, encoding='utf-8')


# Função para coletar e serializar as características
def extract_characteristics(soup):
    characteristics = {}
    
    # Selecionar todas as divs com classe 'flex'
    flex_divs = soup.select('div.flex')
    
    for flex_div in flex_divs:
        # Encontrar todos os <dt> e <dd> dentro da div 'flex'
        dt_elements = flex_div.find_all('dt')
        dd_elements = flex_div.find_all('dd')
        
        # Percorrer os elementos encontrados e extrair título e descrição
        for dt, dd in zip(dt_elements, dd_elements):
            title = dt.get_text(strip=True)
            description = dd.get_text(strip=True)
            
            # Adicionar as características ao dicionário
            characteristics[title] = description
    
    # Serializar as características em JSON
    return json.dumps(characteristics, ensure_ascii=False, indent=4)

# Exemplo de uso
url = 'https://www.lojamaeto.com/lampada-led-200w-bulbo-e40-6500k'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extrair as características e serializá-las em JSON
characteristics_json = extract_characteristics(soup)
print(characteristics_json)

import requests
from bs4 import BeautifulSoup
import json

def extract_product_characteristics(product_url):
    """Extrai as características de um produto a partir da sua URL.

    Args:
        product_url (str): URL da página do produto.

    Returns:
        dict: Dicionário com as características do produto.
    """

    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    characteristics = {}
    # Adaptar os seletores para a estrutura da página de produto
    for flex_div in soup.select('div.flex'):
        dt_elements = flex_div.find_all('dt')
        dd_elements = flex_div.find_all('dd')

        for dt, dd in zip(dt_elements, dd_elements):
            title = dt.get_text(strip=True)
            description = dd.get_text(strip=True)
            characteristics[title] = description

    return characteristics

def scrape_products_and_characteristics(search_term):
    """Rastreia produtos, extrai características e salva em JSON.

    Args:
        search_term (str): Termo de busca.
    """

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

    # Salvar todas as informações em um único arquivo JSON
    with open('produtos.json', 'w') as f:
        json.dump(all_products_data, f, indent=4)


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def classificar_produtos(dados, modelo):
    # Carregar os dados
    data = pd.read_csv("produtos.csv")

    # Separar as features (descrições) e os rótulos (categorias)
    X = data['descricao']
    y = data['categoria']

    # Vetorizar as descrições
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(X)

    # Dividir os dados em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo Naive Bayes
    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    # Prever as categorias para os dados de teste
    y_pred = clf.predict(X_test)

    # Avaliar a precisão do modelo
    accuracy = accuracy_score(y_test, y_pred)
    print("Precisão:", accuracy)

    X = vectorizer.transform(dados['descrição'])

    # Fazer a predição
    previsoes = modelo.predict(X)

    return previsoes

# Exemplo de uso
search_term = "lampada"
scrape_products_and_characteristics(search_term)

import json
from unidecode import unidecode

# Carregar os dados do JSON (supondo que esteja em um arquivo chamado 'dados.json')
def remover_acentos(texto):
    """Remove acentos de uma string.

    Args:
        texto: A string com acentos.

    Returns:
        A string sem acentos.
    """
    return unidecode(texto)

# Carregar os dados do JSON (supondo que esteja em um arquivo chamado 'dados.json')
with open('produtos.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Criar uma nova lista para armazenar os dados sem acentos
dados_sem_acentos = []

# Iterar sobre cada item e remover os acentos
for item in dados:
    novo_item = {}
    for chave, valor in item.items():
        if isinstance(valor, str):
            novo_item[remover_acentos(chave)] = remover_acentos(valor)
        else:
            novo_item[chave] = valor  # Manter valores que não são strings
    dados_sem_acentos.append(novo_item)

# Salvar os dados modificados em um novo arquivo
with open('produtos_formatado.json', 'w', encoding='utf-8') as f:
    json.dump(dados_sem_acentos, f, indent=4)