
import streamlit as st
import pandas as pd
import os
import json
from utils import clasificar_comprobantes, guardar_memory, cargar_memory

# Crear carpeta outputs si no existe
os.makedirs("outputs", exist_ok=True)

# Cargar memory.json
try:
    with open("memory.json", "r") as f:
        memory = json.load(f)
except:
    memory = {}

st.title("Clasificador de Compras AFIP")

uploaded_file = st.file_uploader("Subí tu Excel de compras", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Vista previa de tu archivo:")
    st.dataframe(df.head())

    encabezados = df.columns.tolist()
    col1, col2 = st.columns(2)
    with col1:
        cuit_col = st.selectbox("Seleccioná la columna de CUIT", encabezados)
    with col2:
        proveedor_col = st.selectbox("Seleccioná la columna de Proveedor", encabezados)

    if st.button("Clasificar comprobantes"):
        df_clasificado = clasificar_comprobantes(df, cuit_col, proveedor_col, memory)

        st.write("Comprobantes clasificados:")
        st.dataframe(df_clasificado)

        for index, row in df_clasificado.iterrows():
            nuevo_concepto = st.text_input(f"Concepto para {row[proveedor_col]} ({row['Concepto']})", row['Concepto'], key=index)
            if nuevo_concepto != row['Concepto']:
                df_clasificado.at[index, 'Concepto'] = nuevo_concepto
                memory[row[cuit_col]] = nuevo_concepto

        guardar_memory(memory)

        output_path = f"outputs/clasificado.xlsx"
        df_clasificado.to_excel(output_path, index=False)
        st.success("Clasificación guardada")
        with open(output_path, "rb") as file:
            st.download_button("Descargar Excel Clasificado", file, file_name="clasificado.xlsx")

