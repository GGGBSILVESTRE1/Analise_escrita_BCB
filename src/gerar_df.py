from src.extraction import buscar_atas, extrair_texto_ata
from pathlib import Path
import pandas as pd
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "data" / "raw" / "atas.parquet"


def carregar_dados_base(forcar_atualizacao=False):
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)

    if RAW_PATH.exists() and not forcar_atualizacao:
        print(f"Carregando dados existentes de {RAW_PATH}")
        return pd.read_parquet(RAW_PATH)

    print("Baixando/atualizando dados...")
    df = buscar_atas()

    df = df[df["Url"].notna()]
    df["conteudo_ata"] = df["Url"].apply(extrair_texto_ata)

    if df is None:
        if RAW_PATH.exists():
            print("Falha na coleta. Usando arquivo local existente.")
            return pd.read_parquet(RAW_PATH)
        raise ValueError(
            "Não foi possível coletar os dados e não há arquivo local salvo."
        )

    df = df[df["Url"].notna()].copy()
    df["conteudo_ata"] = df["Url"].apply(extrair_texto_ata)

    df.to_parquet(RAW_PATH, index=False)
    print(f"Dados salvos em {RAW_PATH}")

    return df


if __name__ == "__main__":
    forcar = "--atualizar" in sys.argv
    df = carregar_dados_base(forcar_atualizacao=forcar)
    print(df.head())
