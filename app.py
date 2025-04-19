
import streamlit as st
import pandas as pd
import json
import os
import urllib.parse

from utils import clasificar_comprobantes

# Cargar memoria
if os.path.exists("memory.json"):
    with open("memory.json", "r") as f:
        memory = json.load(f)
else:
    memory = {}

st.title("Clasificador de Compras AFIP")

# Subir archivo
uploaded_file = st.file_uploader("Subí un Excel de compras AFIP", type=["xlsx"])

if uploaded_file is not None:
    if 'df_raw' not in st.session_state:
        st.session_state.df_raw = pd.read_excel(uploaded_file, header=None)

    st.write("Vista previa sin encabezados:")
    st.dataframe(st.session_state.df_raw.head(10))

    encabezado_fila = st.number_input(
        "¿Cuál fila querés usar como encabezado? (empezando desde 0)",
        min_value=0, max_value=len(st.session_state.df_raw)-1, value=0, step=1
    )

    if st.button("Confirmar encabezado"):
        new_header = st.session_state.df_raw.iloc[encabezado_fila]
        df = st.session_state.df_raw[(encabezado_fila+1):]
        df.columns = new_header
        df.reset_index(drop=True, inplace=True)
        st.session_state.df = df

    if 'df' in st.session_state:
        st.write("Vista previa con encabezados seleccionados:")
        st.dataframe(st.session_state.df.head())

        columnas = st.session_state.df.columns.tolist()
        cuit_col = st.selectbox("Seleccioná la columna de CUIT", columnas, key="cuit_col")
        proveedor_col = st.selectbox("Seleccioná la columna de Proveedor", columnas, key="proveedor_col")

        if st.button("Clasificar Comprobantes"):
            df_clasificado = clasificar_comprobantes(st.session_state.df, cuit_col, proveedor_col, memory)

            # Crear carpeta outputs si no existe
            os.makedirs("outputs", exist_ok=True)

            output_path = "outputs/comprobantes_clasificados.xlsx"
            df_clasificado.to_excel(output_path, index=False)
            st.success(f"Archivo clasificado guardado en: {output_path}")
            st.write(df_clasificado)

            for index, row in df_clasificado.iterrows():
                proveedor = row[proveedor_col]
                google_url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(str(proveedor))
                afip_url = "https://www.afip.gob.ar/genericos/guiavirtual/consultas_detalle.aspx?id=3294415"

                st.markdown(f"- [{proveedor} en Google]({google_url}) | [Consulta AFIP]({afip_url})")
