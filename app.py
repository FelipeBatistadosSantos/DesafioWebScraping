from flask import Flask, render_template, request, redirect, url_for
from scraper import scrape_products, save_to_csv
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/', methods=['GET', 'POST'])
def index():
    products = []
    if request.method == 'POST':
        search_term = request.form['search_term']
        products = scrape_products(search_term)

        csv_path = os.path.join('data', 'produtos.csv')
        save_to_csv(products, csv_path)

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
