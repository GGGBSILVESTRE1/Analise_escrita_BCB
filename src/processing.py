import re
from nltk.corpus import stopwords


def limpar_texto_para_tokenizar(texto):

    if not texto:
        return ""

    # converter para minúsculos
    texto = str(texto).lower()
    # retira pontuação mas mantém os caracteres de porcentagem, cifrão, vírgula e ponto
    texto = re.sub(r"[^\w\s%$,.]", "", texto)

    return texto


def tokenizar_texto(texto):

    # transforma string em lista de palavras
    if not texto:
        return []

    stops = set(stopwords.words("portuguese"))

    stops.update(
        [
            "sessões",
            "ata",
            "copom",
            "banco",
            "notas",
            "informações",
            "andar",
            "edifício",
            "central",
            "tabela",
        ]
    )

    palavras = texto.split()

    palavras_limpas = [p for p in palavras if p not in stops and len(p) > 2]

    return palavras_limpas


def limpeza_para_nuvem(tokens):
    return [t for t in tokens if t.isalpha()]
