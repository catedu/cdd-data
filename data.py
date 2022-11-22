import pandas as pd
from collections import OrderedDict
from datetime import datetime
from babel.dates import format_datetime

DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSdo4kxvPecEjGdLdPRSpthqErMLfSME92ZydvcFbSSzexgcN3W_oI_eQ6EL6BqQ8BTnQNoqEShDIW1/pub?gid=1290913514&single=true&output=csv"

NIVEL_DE_PROGRESION = [
    "Conocimiento teórico",
    "Uso guiado",
    "Uso autónomo",
    "Aplicación en el aula",
]

# Create this dict as an ordered dict
int_competencias = {
    1: "A1",
    2: "A2",
    3: "B1",
    4: "B2",
    5: "C1",
    6: "C2",
}


def get_df_competencias(df):
    competencias = pd.read_csv("competencias.csv", sep=",")
    competencias = competencias.rename(
        columns={
            x[0]: x[1]
            for x in zip(competencias.columns[-23:], df.filter(regex="\d\.\d").columns)
        }
    )
    competencias.iloc[:, -23:] = (
        competencias.filter(regex="\d\.\d").fillna(0).astype(int)
    )
    return competencias


def get_df_keywords():
    last_update = format_datetime(
        datetime.now(), 
        "'Última actualización el' EEEE',' d 'de' MMMM 'de' YYYY 'a las' H:mm:ss", 
        locale="es"
        )
    df_keywords = pd.read_csv(DATA_URL, sep=",")
    df_keywords["bag_of_words"] = (
        df_keywords[["PALABRA_CLAVE", "SINONIMOS"]]
        .fillna("")
        .apply(lambda x: x[0].lower().split(",") + x[1].lower().split(","), axis=1)
    )
    df_keywords["bag_of_words"] = df_keywords["bag_of_words"].apply(
        lambda x: [x.strip() for x in x]
    )
    cols = df_keywords.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_keywords = df_keywords.reindex(cols, axis=1)
    return df_keywords, last_update


def get_input_df(df_competencias, lista_niveles):
    niveles_que_faltan = len(df_competencias["COMPETENCIAS AGRUPADAS"]) - len(
        lista_niveles
    )
    lista_niveles.extend([""] * niveles_que_faltan)
    # Generate a Dataframe from two lists
    return pd.DataFrame(
        OrderedDict(
            {
                "Competencias": df_competencias["COMPETENCIAS AGRUPADAS"],
                "Nivel de progresión": lista_niveles,
            }
        )
    )


df_keywords, last_update = get_df_keywords()
df_competencias = get_df_competencias(df_keywords)
input_df = get_input_df(df_competencias, NIVEL_DE_PROGRESION)
