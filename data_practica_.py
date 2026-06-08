#!/usr/bin/env python
# coding: utf-8

# In[2]:


# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3

def extraer_codigo_postal(df, col_origen, col_destino):
    # Patrón RegEx: 5 dígitos continuos para el código postal
    patron_cp = r'(\b\d{5}\b)'
    df[col_destino] = df[col_origen].str.extract(patron_cp)
    return df

def limpiar_telefono(df, col):
    # Patrón RegEx: Elimina símbolos de suma y paréntesis
    patron_limpieza = r'[\+\(\)]'
    df[col] = df[col].str.replace(patron_limpieza, '', regex=True)
    return df

def formatear_fechas(df, col):
    # Agregamos format='mixed' para que Pandas sepa que hay múltiples formatos y no lance la advertencia
    df[col] = pd.to_datetime(df[col], format='mixed', errors='coerce').dt.strftime('%d-%m-%Y')
    return df

def calcular_edad(df, col_nac, col_reg, col_edad):
    # Convierte a datetime para calcular matemáticamente la edad
    fecha_reg = pd.to_datetime(df[col_reg], unit='s', errors='coerce')
    fecha_nac = pd.to_datetime(df[col_nac], format='%d-%m-%Y', errors='coerce')

    # Cálculo de la diferencia en años
    df[col_edad] = (fecha_reg - fecha_nac).dt.days // 365
    df[col_reg] = fecha_reg.dt.strftime('%d-%m-%Y %H:%M:%S')
    return df

def ejecutar_etl():
    csv_url = "https://raw.githubusercontent.com/NationalSpark37/Practica-ETL-part1/refs/heads/main/members%20(2).csv"

    try:
        df = pd.read_csv(csv_url)
    except Exception as e:
        print(f"Error de lectura: {e}")
        return

    # Fase de Transformación (RegEx)
    df = extraer_codigo_postal(df, 'address', 'zip_code')
    df = limpiar_telefono(df, 'phone_number')
    df = formatear_fechas(df, 'birth_date')
    df = calcular_edad(df, 'birth_date', 'register_time', 'edad_registro')

    # Fase de Carga a Base de Datos (SQLite3)
    db_name = "database_LM.db"
    conn = sqlite3.connect(db_name)
    df.to_sql('miembros_transformados', conn, if_exists='replace', index=False)
    conn.close()

    print("ETL Parte 1 completado con éxito.")

if __name__ == "__main__":
    ejecutar_etl()


# In[ ]:




