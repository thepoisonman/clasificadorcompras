
import pandas as pd
import json

def clasificar_comprobantes(df, cuit_col, proveedor_col, memory):
    conceptos = []
    for _, row in df.iterrows():
        cuit = str(row[cuit_col])
        concepto = memory.get(cuit, deducir_concepto(row[proveedor_col]))
        conceptos.append(concepto)
    df['Concepto'] = conceptos
    df['Buscar Google'] = df[cuit_col].apply(lambda cuit: f"https://www.google.com/search?q={cuit}")
    df['Buscar AFIP'] = df[cuit_col].apply(lambda cuit: f"https://www.afip.gob.ar/genericos/guiavirtual/consultas_detalle.aspx?id={cuit}")
    return df

def deducir_concepto(nombre_proveedor):
    nombre = nombre_proveedor.upper()
    if "NAFTA" in nombre or "YPF" in nombre:
        return "Combustible"
    elif "TELECOM" in nombre or "CLARO" in nombre:
        return "Telefonía"
    elif "SUPERMERCADO" in nombre:
        return "Alimentos"
    else:
        return "Otros"

def guardar_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)

def cargar_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {}
