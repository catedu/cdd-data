from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from components import generate_filtered_table, search_inputs_rows, navbar
from data import (
    int_competencias,
    get_df_keywords,
    get_df_competencias,
    number_of_input_rows,
)


def convert_int_to_competencias(df):
    df.iloc[:, -23:] = (
        df.filter(regex="\d\.\d")
        .fillna(0)
        .astype(int)
        .applymap(int_competencias.get)
        .fillna("")
    )
    return df


df_keywords = get_df_keywords()
df_competencias = get_df_competencias()

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
app.title = "Mapeo de actividades"

server = app.server

app.layout = html.Div(
    [navbar]
    + search_inputs_rows
    + [
        html.Br(),
        dbc.Row(
            [
                dbc.Col([html.Div(id="output")]),
            ]
        ),
    ]
)


@app.callback(
    Output("output", "children"),
    [Input(f"palabra-clave-{i}", "value") for i in range(number_of_input_rows)],
)
def show_table(*args):
    print(args)
    if not any(args):
        return html.Div()
    dfs = []
    args = [x for x in args if x]
    for palabra_clave in args:
        palabra_clave = palabra_clave.strip().lower()
        df_filtered = df_keywords.loc[
            df_keywords["bag_of_words"].apply(lambda x: palabra_clave in x),
            df_keywords.filter(regex="\d\.\d").columns,
        ]
        dfs.append(df_filtered)

    df_filtered = pd.concat(dfs, axis=0)

    # Hallamos el valor mayor en cada columna
    serie = df_filtered[df_filtered.filter(regex="\d\.\d").columns].max()

    df_filtered = convert_int_to_competencias(pd.DataFrame(serie).transpose())
    return generate_filtered_table(df_filtered)


if __name__ == "__main__":
    app.run_server(debug=True)
