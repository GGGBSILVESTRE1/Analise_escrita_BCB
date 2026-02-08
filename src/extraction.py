from urllib import response
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time

BASE_URL = "https://www.bcb.gov.br"

def buscar_atas():
    url = "https://www.bcb.gov.br/api/servico/sitebcb/atascopom/ultimas?quantidade=100&filtro=Id%20ne%20%27258%27"
    print(f"DEBUG: Acessando URL: {url}") 

    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"DEBUG: Status Code: {response.status_code}")
        
        dados = response.json()
        print(f"DEBUG: Chaves do JSON: {dados.keys()}") 
        
        lista_atas = dados.get('conteudo', [])
        print(f"DEBUG: Quantidade de itens encontrados: {len(lista_atas)}")

        df = pd.DataFrame(lista_atas)
        return df

    except Exception as e:
        print(f"DEBUG: Ocorreu um erro: {type(e).__name__} - {e}")
        return None
    



def extrair_texto_ata(url_ata):
    try: 
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get( BASE_URL + url_ata, headers=headers, timeout = 10)
        time.sleep(random.uniform(1, 2))
        if response.status_code != 200:
            print(f"DEBUG: falha ao acessar {url_ata}, status code: {response.status_code}")
            return None
        

        if url_ata.lower().endswith('.pdf'):
            return "pdf_ignorado"
        

        soup = BeautifulSoup(response.content, 'html.parser')
        
        paragrafos = soup.get_text(strip=True)
        texto_limpo = '\n'.join([p.strip() for p in paragrafos.split('\n') if len(p.strip()) > 5])

        return texto_limpo 
    
    except Exception as e:
        print(f"DEBUG: Erro ao extrair texto da ata: {type(e).__name__} - {e}")
        print(f"Erro ao raspar {url_ata}: {e}")
        return None
    
