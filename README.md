# 🛒 Web Scraping - Lojas Maeto

Este projeto realiza a raspagem de dados de produtos do site Lojas Maeto e disponibiliza os dados em formato CSV e JSON.

## 🛠️ Requisitos

Antes de iniciar o projeto, você precisa configurar um ambiente virtual e instalar as dependências.

### 🔧 Configurando o Ambiente

1. **Crie e ative um ambiente virtual:**

   No terminal, execute:
   python -m venv venv

2. **Ative o ambiente virtual:**

- Windows:
    .\venv\Scripts\activate
    ou 
    venv\Scripts\activate

- MacOS/Linux:
    source venv/bin/activate

3. **Instale as dependências:**

    Execute este código no terminal:

    pip install -r requirements.txt

# 🚀 **Executando o Projeto**

4. Inicie o servidor flask:
    Execute este código no terminal:

    python src/app.py

5. Acesse a aplicação:

    Abra seu navegador e vá para http://127.0.0.1:5000 para usar a aplicação.

# 📁 Estrutura do Projeto
 - src/app.py: Código principal do aplicativo Flask.
 - src/scraper.py: Código responsável pela raspagem de dados.
 - templates/index.html: Arquivo HTML para a interface web.
 - requirements.txt: Lista de pacotes Python necessários.
 - data/: Diretório onde os arquivos CSV e JSON são salvos.
 
# ⚠️ Observações
Certifique-se de ter o Python instalado.





