import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
from transformers import pipeline, auto_tokenizer, AutoModelForSequenceClassification

classifier = pipeline("sentiment-analysis", model="lucas-leme/FinBERT-PT-BR")

load_dotenv()


# implementação básica para um comparativo com o modelo de classificação de sentimento tradicional
def hawkish_dovish(token):

    hawkish = [
        "inflacao",
        "pressões inflacionarias",
        "inflação persistente",
        "risco inflacionário",
        "risco",
        "contracionista",
        "aquecido",
        "elevacao",
    ]
    dovish = [
        "desinflaçao",
        "queda da inflação",
        "flexibilizaçao monetaria",
        "queda",
        "recuo",
        "desaceleraçao",
        "estabilidade",
        "flexibilizacao",
        "corte",
    ]

    hawkish_count = sum(token.count(word) for word in hawkish)
    dovish_count = sum(token.count(word) for word in dovish)

    score = (hawkish_count - dovish_count) / (hawkish_count + dovish_count)

    return score
