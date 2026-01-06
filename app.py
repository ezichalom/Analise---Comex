import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Comex", layout="wide")

st.title("📊 Dashboard de Exportações - ComexStat")
st.markdown("Upload do Excel do ComexStat (abas por ano)")

uploaded_file = st.file_uploader("Upload do arquivo Excel", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    abas = xls.sheet_names

    lista = []

    for aba in abas:
        df = pd.read_excel(uploaded_file, sheet_name=aba)
        df.columns = df.columns.str.strip()

        df["Ano/Mês"] = pd.to_datetime(df["Ano/Mês"])
        df["Ano"] = df["Ano/Mês"].dt.year
        df["Mês"] = df["Ano/Mês"].dt.month

        lista.append(df)

    base = pd.concat(lista, ignore_index=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        ano = st.multiselect("Ano", sorted(base["Ano"].unique()), sorted(base["Ano"].unique()))

    with col2:
        pais = st.multiselect("País", sorted(base["País"].unique()))

    with col3:
        ncm = st.multiselect("NCM", sorted(base["NCM"].unique()))

    df = base[base["Ano"].isin(ano)]

    if pais:
        df = df[df["País"].isin(pais)]
    if ncm:
        df = df[df["NCM"].isin(ncm)]

    metrica = st.radio("Métrica", ["Valor FOB", "Peso Líquido"], horizontal=True)

    resumo = df.groupby(["Ano", "Mês"], as_index=False)[metrica].sum()

    fig = px.line(
        resumo,
        x="Mês",
        y=metrica,
        color="Ano",
        markers=True,
        title=f"Comparativo Anual - {metrica}"
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Base Consolidada"):
        st.dataframe(df)
