import os

from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_auth
import pandas as pd

VALID_USERNAME_PASSWORD_PAIRS = {os.environ.get("USER"): os.environ.get("PASSWORD")}

from components import (
    search_inputs_rows,
    navbar,
    generate_bootstrap_table,
)
from data import (
    df_keywords,
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
    if palabras_clave is None or len(palabras_clave) == 0:
        return html.Div()
    df_filtered = filtrar_por_palabras_clave(palabras_clave, df_keywords)
    if modalidad:
        # TODO: filtro por modalidad quitando datos
        df_filtered = segun_modalidad(df_filtered, modalidad)

    # obtengo los datos de la tabla de Competencias y Nivel de progresión
    rows_filtered = [
        (row.get("competencias"), row.get("nivel-de-progresion")) for row in rows
    ]
    df_filtered = modifica_segun_competencias(
        df_filtered, df_competencias, rows_filtered
    )
    df_filtered = add_cdd_minimum(df_filtered)
    if not actividad_con_alumnado:
        df_filtered = con_alumnado(df_filtered)
    if horas:
        df_filtered = to_a2_if_below_10(df_filtered)
    df_filtered = convert_int_to_competencias(df_filtered)
    return generate_bootstrap_table(df_filtered), str(rows_filtered)


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


if __name__ == "__main__":
    app.run_server(debug=True)
