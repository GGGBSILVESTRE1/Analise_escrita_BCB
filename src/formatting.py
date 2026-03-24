import re
from transformers import pipeline


def data_formatada(data):
    s = str(data)
    s = s.replace("T", " ")
    s = s.replace("-", "")
    s = s.replace("Z", "")

    return s


def limpar_texto(texto):
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    texto = re.sub(r"[ \t]+\n", "\n", texto)
    texto = re.sub(r"\n[ \t]+", "\n", texto)
    texto = re.sub(r"\s{2,}", " ", texto)
    return texto.strip()


def get_sentiment_bert(texto):
    model_name = "lucas-leme/FinBERT-PT-BR"
    return pipeline("sentiment-analysis", model=model_name, device="cpu")
