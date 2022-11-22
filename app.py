import os
import contextlib

from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_auth
import pandas as pd
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

print(os.environ.get("DEBUG"))

VALID_USERNAME_PASSWORD_PAIRS = {os.environ.get("APPUSER"): os.environ.get("PASSWORD")}

from components import (
    search_inputs_rows,
    navbar,
    generate_bootstrap_table,
)
from data import (
    get_df_keywords,
    df_keywords,
    last_update,
    df_competencias,
)
from utils import (
    filtrar_por_palabras_clave,
    to_a2_if_below_10,
    convert_int_to_competencias,
    segun_modalidad,
    con_alumnado,
    modifica_segun_competencias,
    add_cdd_minimum,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
app.title = "Mapeo de actividades"
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

server = app.server

app.layout = html.Div(
    [navbar]
    + search_inputs_rows
    + [
        html.Br(),
        dbc.Row(
            [
                dbc.Col([html.Div(id="output")]),
            ],
            justify="center",
        ),
    ]
)


@app.callback(
    Output("output", "children"),
    Input(
        "palabras-clave",
        "value",
    ),
    Input("menos-de-10-horas", "value"),
    Input(
        "modalidad",
        "value",
    ),
    Input(
        "bool-con-alumnado",
        "value",
    ),
    Input(
        "adding-rows-table",
        "derived_viewport_data",
    ),
)
def show_table(palabras_clave, horas, modalidad, actividad_con_alumnado, rows):
    try:
        rows_filtered = [
            (row.get("competencias"), row.get("nivel-de-progresion")) for row in rows
        ]
    except:
        pass
    if palabras_clave is None or len(palabras_clave) == 0:
        df_filtered = filtrar_por_palabras_clave("nada,nada", df_keywords)
    else:
        df_filtered = filtrar_por_palabras_clave(palabras_clave, df_keywords)
    df_filtered = modifica_segun_competencias(
        df_filtered, df_competencias, rows_filtered
    )
    if modalidad:
        # TODO: filtro por modalidad quitando datos
        df_filtered = segun_modalidad(df_filtered, modalidad)

    # obtengo los datos de la tabla de Competencias y Nivel de progresión
    df_filtered = add_cdd_minimum(df_filtered)
    if not actividad_con_alumnado:
        df_filtered = con_alumnado(df_filtered)
    if horas:
        df_filtered = to_a2_if_below_10(df_filtered)
    df_filtered = convert_int_to_competencias(df_filtered)
    return generate_bootstrap_table(df_filtered)


@app.callback(
    Output("adding-rows-table", "data"),
    Input("editing-rows-button", "n_clicks"),
    State("adding-rows-table", "data"),
    State("adding-rows-table", "columns"),
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(
    Output("output-last-update", "children"), [Input("refresh-data", "n_clicks")]
)
def refresh_data(value):
    global df_keywords, last_update
    df_keywords, last_update = get_df_keywords()
    return last_update


if __name__ == "__main__":
    app.run_server(debug=bool(os.environ.get("DEBUG")))
