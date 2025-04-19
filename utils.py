import pandas as pd

def clasificar_comprobantes(df, cuit_col, proveedor_col, memory):
    df['Concepto'] = df[proveedor_col].apply(lambda x: memory.get(x, 'Otros'))
    return df
