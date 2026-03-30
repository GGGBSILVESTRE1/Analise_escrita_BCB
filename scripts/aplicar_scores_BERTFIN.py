from src.processing_bert import processar_atas_individual
import pandas as pd
import os


def processar_atas():

    RAW_PATH = "data/raw/atas.parquet"
    PROCESSED_PATH = "data/processed/Scores_BERTFIN.parquet"

    df_raw = pd.read_parquet(RAW_PATH)

    # lógica para evitar reprocessamento de atas já processadas em execuções anteriores do script, garantindo eficiência e economia de recursos computacionais
    if os.path.exists(PROCESSED_PATH):
        df_ja_processado = pd.read_parquet(PROCESSED_PATH)

        # utilizando Titulo  referencia como chave para identificar quais atas já foram processadas, evitando reprocessamento desnecessário
        processados_ids = df_ja_processado["Titulo"].tolist()
        df_para_processar = df_raw[~df_raw["Titulo"].isin(processados_ids)]

    else:
        df_para_processar = df_raw.copy()
        df_ja_processado = pd.DataFrame(
            columns=["Titulo", "positivo", "negativo", "neutro"]
        )

    if df_para_processar.empty:
        return df_ja_processado

    df_para_processar["sentimento_temp"] = df_para_processar["conteudo_ata"].apply(
        processar_atas_individual
    )

    df_sentimentos = df_para_processar["sentimento_temp"].apply(pd.Series)

    df_final = pd.concat(
        [
            df_para_processar[["Titulo"]].reset_index(drop=True),
            df_sentimentos.reset_index(drop=True),
        ],
        axis=1,
    )

    df_final_completo = pd.concat([df_ja_processado, df_final], ignore_index=True)

    df_final_completo.to_parquet(PROCESSED_PATH)

    return df_final_completo


if __name__ == "__main__":
    df_processado = processar_atas()
    print(df_processado)
