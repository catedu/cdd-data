from typing import List

import pandas as pd
from data import int_competencias

def convert_to_one_row_df_with_max_values(dfs: List):
    df_filtered = pd.concat(dfs, axis=0)
    # Hallamos el valor mayor en cada columna
    serie = df_filtered[df_filtered.filter(regex="\d\.\d").columns].max()
    return pd.DataFrame(serie).transpose()

def convert_int_to_competencias(df):
    df.iloc[:, -23:] = (
        df.filter(regex="\d\.\d")
        .fillna(0)
        .astype(int)
        .applymap(int_competencias.get)
        .fillna("")
    )
    return df

def to_a2_if_below_10(df):
    """Check all the cells with values and values greater than 2 and set them to 1"""
    df.iloc[:, -23:] = (
        df.filter(regex="\d\.\d")
        .applymap(lambda x: 1 if x > 2 else x)
    )
    return df

def filtrar_por_palabras_clave(palabras_clave: str, df: pd.DataFrame):
    """Filtrar por palabras clave"""
    dfs = []
    palabras_clave = list(palabras_clave.split(","))
    palabras_clave = [x.strip() for x in palabras_clave if len(x.strip()) > 0]
    for palabra_clave in palabras_clave:
        palabra_clave = palabra_clave.strip().lower()
        df_filtered = df.loc[
            df["bag_of_words"].apply(lambda x: palabra_clave in x),
            df.filter(regex="\d\.\d").columns,
        ]
        dfs.append(df_filtered)
        
    return convert_to_one_row_df_with_max_values(dfs)

def segun_modalidad(df, modalidad):
    """Si la modalidad es "Grupo de trabajo" se fija el valor 3 si la celda tiene valor en las columnas que empiecen por "2." """
    if modalidad == 4:
        df[df.filter(regex="2\.\d").columns] = (
            df.filter(regex="2\.\d")
            .applymap(lambda x: 3 if x > 0 else x)
        )
    else:
        df["1.2"] = 2
        df["1.4"] = 3
        
    return df

def con_alumnado(df):
    """Asigna el valor 0 en las columnas que empiecen por "6." """
    df[df.filter(regex="6\.\d").columns] = 0
    return df

def modifica_segun_competencias(df, df_competencias, rows):
    """"""
    pass
        