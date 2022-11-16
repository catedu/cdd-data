from pprint import pprint

from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from components import generate_filtered_table, search_inputs_rows, navbar
from data import (
    get_df_keywords,
    df_competencias,
)
from utils import (
    filtrar_por_palabras_clave, 
    to_a2_if_below_10, 
    convert_int_to_competencias,
    segun_modalidad,
    con_alumnado,
    modifica_segun_competencias,
    )


df_keywords = get_df_keywords()

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
    Input(
        "palabras-clave",
        "value",
    ),
    Input(
        "menos-de-10-horas",
        "value"
    ),
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
    )
)
def show_table(palabras_clave, horas, modalidad, actividad_con_alumnado, rows):
    rows = [(row.get("competencias"), row.get("nivel-de-progresion")) for row in rows]
    if palabras_clave is None or len(palabras_clave) == 0:
        return html.Div()
    df_filtered = filtrar_por_palabras_clave(palabras_clave, df_keywords)
    if horas:
        df_filtered = to_a2_if_below_10(df_filtered)
    if modalidad:
        # TODO: filtro por modalidad quitando datos
        df_filtered = segun_modalidad(df_filtered, modalidad)
    if not actividad_con_alumnado:
        df_filtered = con_alumnado(df_filtered)
    # df_filtered = modifica_segun_competencias(df_filtered, df_competencias, rows)
    df_filtered = convert_int_to_competencias(df_filtered)
    return generate_filtered_table(df_filtered)


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
