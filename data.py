import pandas as pd
from collections import OrderedDict

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
    return pd.read_csv("competencias.csv", sep=",")


def get_df_keywords():
    df_keywords = pd.read_csv("Dicc.csv", sep=";")
    df_keywords["bag_of_words"] = (
        df_keywords[["PALABRA_CLAVE", "SINONIMOS"]]
        .fillna("")
        .apply(lambda x: x[0].lower().split(",") + x[1].lower().split(","), axis=1)
    )
    df_keywords["bag_of_words"] = df_keywords["bag_of_words"].apply(
        lambda x: [x.strip() for x in x]
    )
    return df_keywords


def get_input_df():
    pass
