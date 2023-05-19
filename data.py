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

NOMBRES_COMPETENCIAS = [
    {"1.1": "Comunicación organizativa"},
    {"1.2": "Participación, colaboración y coordinación profesional"},
    {"1.3": "Práctica reflexiva"},
    {"1.4": "Desarrollo profesional digital continuo (DPC)"},
    {"1.5": "Protección de datos personales, privacidad, seguridad y bienestar digital"},
    {"2.1": "Búsqueda y selección de contenidos digitales"},
    {"2.2": "Creación y modifciación de contenidos digitales"},
    {"2.3": "Protección, gestión y compartición de contenidos digitales"},
    {"3.1": "Enseñanza"},
    {"3.2": "Orientación y apoyo en el aprendizaje"},
    {"3.3": "Aprendizaje entre iguales"},
    {"3.4": "Aprendizaje autorregulado"},
    {"4.1": "Recogida de datos a traves de herramientas digitales"},
    {"4.2": "Analizar, organizar e interpretar esos datos con herramientas digitales"},
    {"4.3": "Retroalimentación del proceso de E-A. usando herramientas digitales"},
    {"5.1": "Accesibilidad e inclusión"},
    {"5.2": "Atención a las diferencias personales en el aprendizaje"},
    {"5.3": "Compromiso activo del alumnado con su propio aprendizaje"},
    {"6.1": "Alfabetización mediática y en tratamiento de la información y de los datos"},
    {"6.2": "Comunicación, colaboración y ciudadanía digital"},
    {"6.3": "Creación de contenidos digitales"},
    {"6.4": "Uso responsable y bienestar digital"},
    {"6.5": "Resolución de problemas"},
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


def get_df_competencias():
    competencias = pd.read_csv("competencias.csv", sep=",")
    competencias.iloc[:, -23:] = (
        competencias.filter(regex="\d\.\d").fillna(0).astype(int)
    )
    return competencias


def get_df_keywords():
    last_update = format_datetime(
        datetime.now(),
        "'Última actualización el' EEEE',' d 'de' MMMM 'de' YYYY 'a las' H:mm:ss",
        locale="es",
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
df_competencias = get_df_competencias()
input_df = get_input_df(df_competencias, NIVEL_DE_PROGRESION)
