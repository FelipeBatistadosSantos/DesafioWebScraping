from flask import Flask, render_template, request, redirect, url_for
from scraper import scrape_products
import csv
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods=['GET', 'POST'])
def index():
    products = []  # Inicializa products como uma lista vazia
    
    if request.method == 'POST':
        search_term = request.form['search_term']
        products = scrape_products(search_term)

        csv_path = os.path.join('data', 'produtos.csv')
        if not os.path.exists('data'):
            os.makedirs('data')

        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Nome', 'Preço Antigo', 'Preço Pix', 'Preço Cartão', 'URL Imagem']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow(product)

        # Renderiza a página com a lista de produtos
        return render_template('index.html', products=products)

    # Em caso de GET, apenas renderiza a página inicial
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
