import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math
from datetime import datetime

url = 'https://www.cec.com.br/material-de-construcao'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens = soup.find('span', id='Body_Body_lblCount').get_text().strip()

index = qtd_itens.find(' ')
qtd = qtd_itens[:index]

ultima_pagina = math.ceil(int(qtd)/ 24)

dicProdutos = {'nome_Produto_Coleta':[], 'preco_Coleta':[], 'codigo_Produto': [], 'arquivo_do_preco': [], 'url_Produto': [], 'data_Coleta':[]}

for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.cec.com.br/material-de-construcao?page={i}'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('product '))
    

    for produto in produtos:
        nome_Produto_Coleta = produto.find('a', class_=re.compile('name-and-brand')).get_text().strip()
        preco_Coleta = produto.find('span', class_=re.compile('value-full')).get_text().strip()
        hora = datetime.now()
        codigo_Produto = produto.get('data-product-id')

        hard_Produto = produto.find('a', class_='name-and-brand')
        url_Produto = hard_Produto.get('href')

        img_Produto = produto.find('img', itemprop=re.compile('image'))
        arquivo_do_preco = img_Produto.get('src')

        print(nome_Produto_Coleta, preco_Coleta, hora, codigo_Produto)

        dicProdutos['codigo_Produto'].append(codigo_Produto)
        dicProdutos['nome_Produto_Coleta'].append(nome_Produto_Coleta)
        dicProdutos['preco_Coleta'].append(preco_Coleta)
        dicProdutos['arquivo_do_preco'].append(arquivo_do_preco)
        dicProdutos['url_Produto'].append(f"https://www.cec.com.br{url_Produto}")
        dicProdutos['data_Coleta'].append(hora)
        
    print(url_pag)

df = pd.DataFrame(dicProdutos)
df.to_csv('C:/Users/cesar/OneDrive/Área de Trabalho/Dados WebScraping/produtos_Coleta.csv', encoding='utf-8', sep=';')