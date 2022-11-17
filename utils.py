from typing import List
from pprint import pprint

import pandas as pd
from data import int_competencias, NIVEL_DE_PROGRESION


def add_cdd_minimum(df: pd.DataFrame):
    """Añadir valores mínimos por tratarse formación CDD"""
    df["1.3"] = df["1.3"].apply(lambda x: 1 if x == 0 else x)
    df[["1.1", "1.4", "1.5"]] = df[["1.1", "1.4", "1.5"]].applymap(lambda x: max(x, 2))
    df["3.1"] = df["3.1"].apply(lambda x: 1 if x == 0 else x)
    return df


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
    df.iloc[:, -23:] = df.filter(regex="\d\.\d").applymap(lambda x: 1 if x > 2 else x)
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
        df[df.filter(regex="2\.\d").columns] = df.filter(regex="2\.\d").applymap(
            lambda x: 3 if x > 0 else x
        )
    else:
        df["1.2"] = df["1.2"].apply(lambda x: max(x, 2))
        df["1.4"] = df["1.4"].apply(lambda x: max(x, 3))

    return df


def con_alumnado(df):
    """Asigna el valor 0 en las columnas que empiecen por "6." """
    df[df.filter(regex="6\.\d").columns] = 0
    return df


def modifica_segun_competencias(df_filtered, df_competencias, rows):
    """"""
    modifiers = {item: i + 1 for i, item in enumerate(NIVEL_DE_PROGRESION)}

    dfs = []
    for row in rows:
        if row[0] is None or row[1] is None:
            continue
        df = df_competencias.loc[
            df_competencias["COMPETENCIAS AGRUPADAS"] == row[0],
            df_competencias.filter(regex="\d\.\d").columns,
        ]
        df.to_csv("test.csv")
        df = df.applymap(lambda x: x if x == 0 else modifiers[row[1]])
        df.to_csv("test2.csv")
        dfs.append(df)

    dfs.append(df_filtered)

    return convert_to_one_row_df_with_max_values(dfs)
