import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


nltk.download("punkt")  # modelo de tokenização pré treinado
nltk.download("punkt_tab")
nltk.download("stopwords")  # lista de palavras comuns que não agregam valor semântico


def tokenize_text(texto):

    texto = texto.lower()

    tokens = word_tokenize(texto, language="portuguese")

    palavras_irrelevantes = set(stopwords.words("portuguese"))
    pontuacao = set(string.punctuation)

    palavras_extras = {"copom", "banco", "central", "Comitê", "bcb.gov.br", "reuniao"}

    palavras_irrelevantes.update(palavras_extras)

    tokens_filtrados = [
        t
        for t in tokens
        if t not in palavras_irrelevantes
        and t not in pontuacao
        and len(t) > 2
        and t.isalpha()
    ]

    return tokens_filtrados
