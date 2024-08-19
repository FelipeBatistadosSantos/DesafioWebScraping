from flask import Flask, render_template, request, send_from_directory
from scraper import scrape_all_pages, save_to_csv, save_to_json
import os

app = Flask(__name__, template_folder='../templates')

search_count = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    global search_count
    products = []
    csv_filename = ""
    json_filename = ""
    if request.method == 'POST':
        search_term = request.form['search_term']
        products = scrape_all_pages(search_term)

        csv_filename = save_to_csv(products, search_term, search_count)
        json_filename = save_to_json(products, search_term, search_count)
        
        search_count += 1

    return render_template('index.html', products=products, search_term=request.form.get('search_term', ''), search_count=search_count)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('data', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
