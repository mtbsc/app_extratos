import pandas as pd

def c6_formater(arquivo):

    df_csv = pd.read_csv(arquivo, sep=";") # transformarndo o csv em dataframe, esse usa ";" como separador

    df_csv = df_csv.drop(columns=[
        "Nome no Cartão",
        "Final do Cartão",
        "Categoria",
        "Parcela",
        "Valor (em US$)",
        "Cotação (em R$)"
    ], errors="ignore") # deletando colunas desnecessárias

    # renomeando colunas para ficar igual do powerbi
    df_csv = df_csv.rename(columns = {"Valor (em R$)": "VALOR"})
    df_csv = df_csv.rename(columns = {"Data de Compra": "DATA"})
    df_csv = df_csv.rename(columns = {"Descrição": "ITEM"})
    #

    df_csv["VALOR"] = df_csv["VALOR"].astype(float) # transformando VALOR em número para filtrar negativos

    df_csv = df_csv[df_csv["VALOR"] > 0] # apagando os valores positivos (estamos contando só os gastos)
    df_csv = df_csv.reset_index(drop=True) # resetar o index para o numero de linhas ficar bonitinho

    df_csv["VALOR"] = df_csv["VALOR"].apply(lambda x: f"{x:.2f}".replace(".", ",")) #trocando o separador decimal de ponto pra vírgula (brasileiro)

    df_csv["ITEM"] = df_csv["ITEM"].apply(lambda x: str(x).split(" - ")[-1].strip()) #removendo a descrição que vem antes do "-" (geralmente é algo do tipo 'compra no débito')

    # criando colunas que faltam (categoria, pessoa e cartão)
    df_csv["PESSOA"] = ""
    df_csv["CARTÃO"] = "C6"
    df_csv["CATEGORIA"] = ""
    #

    # reordenando coluna pra ficar na mesma ordem do bi
    cols = ["DATA", "ITEM", "VALOR", "PESSOA", "CARTÃO", "CATEGORIA"]
    df_csv = df_csv[cols]
    #

    # reordenando coluna pra ficar na mesma ordem do bi
    cols = df_csv.columns.tolist()
    cols = [cols[1], cols[5], cols[3], cols[0], cols[4], cols[2]]
    df_csv = df_csv[cols]
    #

    return df_csv

def nb_formater(arquivo):

    df_csv = pd.read_csv(arquivo, sep=",") # transformarndo o csv em dataframe

    df_csv = df_csv.drop(columns=["Identificador"]) # deletando a coluna identificador

    df_csv = df_csv[df_csv["Valor"] < 0] # apagando os valores positivos (estamos contando só os gastos

    df_csv = df_csv.reset_index(drop=True) # resetar o index para o numero de linhas ficar bonitinho

    df_csv["Valor"] = df_csv["Valor"].abs() # transformando os valores negativos em numeros positivos (absoluto)

    df_csv["Valor"] = df_csv["Valor"].apply(lambda x: str(x).replace(".", ",")) #trocando o separador decimal de ponto pra vírgula (brasileiro)

    # renomeando colunas para ficar igual do powerbi
    df_csv = df_csv.rename(columns = {"Valor": "VALOR"})
    df_csv = df_csv.rename(columns = {"Data": "DATA"})
    df_csv = df_csv.rename(columns = {"Descrição": "ITEM"})
    #

    df_csv["ITEM"] = df_csv["ITEM"].apply(lambda x: str(x).split(" - ")[-1].strip()) #removendo a descrição que vem antes do "-" (geralmente é algo do tipo 'compra no débito')

    # criando colunas que faltam (categoria, pessoa e cartão)
    df_csv["PESSOA"] = ""
    df_csv["CARTÃO"] = "NUBANK"
    df_csv["CATEGORIA"] = ""

    # reordenando coluna pra ficar na mesma ordem do bi
    cols = df_csv.columns.tolist()
    cols = [cols[2], cols[5], cols[3], cols[0], cols[4], cols[1]]
    df_csv = df_csv[cols]
    #

    return df_csv
