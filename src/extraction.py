from src.formatting import limpar_texto
import requests
import pandas as pd
import fitz
import io


BASE_URL = "https://www.bcb.gov.br"


def buscar_atas():
    url = "https://www.bcb.gov.br/api/servico/sitebcb/atascopom/ultimas?quantidade=100&filtro=Id%20ne%20%27258%27"
    print(f"DEBUG: Acessando URL: {url}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"DEBUG: Status Code: {response.status_code}")

        dados = response.json()
        print(f"DEBUG: Chaves do JSON: {dados.keys()}")

        lista_atas = dados.get("conteudo", [])
        print(f"DEBUG: Quantidade de itens encontrados: {len(lista_atas)}")

        df = pd.DataFrame(lista_atas)
        return df

    except Exception as e:
        print(f"DEBUG: Ocorreu um erro: {type(e).__name__} - {e}")
        return None


def extrair_texto_ata(url_ata):

    if not isinstance(url_ata, str):
        return None
    try:
        url_ata = str(url_ata)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(BASE_URL + url_ata, headers=headers, timeout=20)
        if response.status_code != 200:
            print(
                f"DEBUG: falha ao acessar {url_ata}, status code: {response.status_code}"
            )
            return None

        if response.status_code == 200:
            with fitz.open(stream=io.BytesIO(response.content), filetype="pdf") as doc:
                texto_pagina = []
                for pagina in doc:
                    texto_pagina.append(pagina.get_text())

                texto_completo = "\n".join(texto_pagina)

                texto_limpo = limpar_texto(texto_completo)

                return texto_limpo

        else:
            print(
                f"DEBUG: falha ao biaxar o pdf {url_ata}, status code: {response.status_code}"
            )
            return None

    except Exception as e:
        print("Erro na extração do PDF:", e)
        return None
