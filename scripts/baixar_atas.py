from src.extraction import buscar_atas, extrair_texto_ata


def coletar_dados():

    df = buscar_atas()

    if df is None:
        print("Erro ao buscar as atas")
        return

    df = df[df["Url"].notna()]
    df["conteudo_ata"] = df["Url"].apply(extrair_texto_ata)

    return df


def salvar_dados():

    df = coletar_dados()

    if df is not None:
        df.to_parquet("data/raw/atas.parquet", index=False)


if __name__ == "__main__":
    salvar_dados()
