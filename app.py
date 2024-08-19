from flask import Flask, render_template, request, send_from_directory
from scraper import scrape_products, save_to_csv
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Iniciar o contador de pesquisa
search_count = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    global search_count
    products = []
    csv_filename = ""
    if request.method == 'POST':
        search_term = request.form['search_term']
        products = scrape_products(search_term)

        # Salvar em CSV usando o contador de pesquisa
        csv_filename = save_to_csv(products, search_term, search_count)
        
        # Incrementar o contador de pesquisa para a próxima busca
        search_count += 1

    return render_template('index.html', products=products, search_term=request.form.get('search_term', ''), search_count=search_count, csv_filename=csv_filename)

@app.route('/download/<filename>')
def download_file(filename):
    # Caminho para o diretório de arquivos
    return send_from_directory('data', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
