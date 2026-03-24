from src.processing import processar_atas_individual


def processar_atas(df):

    df["sentimento"] = df["conteudo_ata"].apply(processar_atas_individual)

    df["score_positivo"] = df["sentimento_detalhado"].apply(
        lambda x: x["positivo"] if x else 0
    )

    return df
