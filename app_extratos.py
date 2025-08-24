import streamlit as st
import pandas as pd
from io import BytesIO, StringIO

# importar as funções
from functions import nb_formater, c6_formater

# essa gambiarra é pra ver se o arquivo é c6 ou nubank (nubank tem separadores ',' e c6 usa ';'.)
def detectar_sep(arquivo_str):
    arquivo_str.seek(0)
    primeira_linha = arquivo_str.readline().decode("utf-8")
    arquivo_str.seek(0)

    if primeira_linha.count(";") > primeira_linha.count(","):
        return ";"
    else:
        return ","

# aqui detecta qual banco é, com a ajuda de detectar_sep e inicia a função correspondente
def detectar_banco(arquivo):
    file_bytes = arquivo.read()
    arquivo_bytes = BytesIO(file_bytes) # transformar o upload do streamlit em arquivo
    sep = detectar_sep(arquivo_bytes)

    # transformar em string pro pandas ler
    texto = file_bytes.decode("utf-8")
    arquivo_str = StringIO(texto)

    # checar qual separador é usado
    if sep == ";":
        return c6_formater(arquivo_str)
    elif sep == ",":
        return nb_formater(arquivo_str)
    else:
        raise ValueError("Arquivo não reconhecido.")




st.set_page_config(page_title = "App_extratos", layout="wide")
st.title("App_extratos")
"""
App_extratos é um programa que organiza arquivos CSV de extratos do Nubank e C6 (por enquanto) em um formato de tabela compatível para o Power BI.
Fiz isso pra ajudar a organizar minhas finanças e da conja.
"""
st.markdown("PS: As colunas CATEGORIA e PESSOA são deixadas em branco para serem preenchidas manualmente depois")
st.markdown("Faça upload dos CSVs:")

# para fazer upload dos arquivos
arquivos = st.file_uploader("Envie seus CSVs", type="csv", accept_multiple_files=True)

# botão para processar arquivos
if st.button("Processar Arquivos"):
    if not arquivos:
        st.warning("Envie pelo menos um arquivo.")
    else:
        frames = []
        erros = []

        for arq in arquivos:
            try:
                df = detectar_banco(arq)
                frames.append(df)
            except Exception as erro:
                erros.append(f"{arq.name}: {erro}")

        if erros:
            st.error("Ocorreram erros em alguns arquivos:")
            for e in erros:
                st.write(e)

        if frames:
            df_all = pd.concat(frames, ignore_index=True)
            df_all["DATA"] = pd.to_datetime(df_all["DATA"], dayfirst=True, errors="coerce") # deixar no formato data brasileira

            # estatisticas legais
            c1, c2, c3 = st.columns(3)
            c1.metric("Transações", len(df_all))
            c2.metric("Total", f"{df_all['VALOR'].str.replace(',','.', regex=False).astype(float).sum():.2f}")
            c3.metric(
                "Período",
                f"{df_all['DATA'].min().strftime('%d/%m/%Y')} — {df_all['DATA'].max().strftime('%d/%m/%Y')}"
            )

            st.subheader("Prévia")
            df_preview = df_all.copy()
            df_preview["DATA"] = df_preview["DATA"].dt.strftime("%d/%m/%Y")
            st.dataframe(df_preview.head(50))

            # escrevendo o arquivo excel
            buffer = BytesIO()
            with pd.ExcelWriter(
                    buffer,
                    engine="xlsxwriter",
                    date_format="dd/mm/yyyy",
                    datetime_format="dd/mm/yyyy"
            ) as writer:
                df_tmp = df_all.copy()
                df_tmp["DATA"] = df_tmp["DATA"].dt.date  # garante só a data
                df_tmp.to_excel(writer, index=False, sheet_name="dados")

            # botão de download
            st.download_button(
                "Baixar Excel",
                data=buffer.getvalue(),
                file_name="contas_do_mes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )


