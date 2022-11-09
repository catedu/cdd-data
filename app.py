from pathlib import Path

from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pandas as pd

from components import navbar, generate_table

DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR-BAUvNUjp2AeV_daeeqHReX0M3ew3ZpEL3nfkrz96uUd816mV_hV1uWMvbsACphEBGjqHJBswGwFz/pub?gid=614465369&single=true&output=csv"
    

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

server = app.server

def get_data():
    if not Path("data.csv").exists():
        pd.read_csv(DATA_URL).to_csv("data.csv", index=False)
    df = pd.read_csv("data.csv")
    df = df[(df["Curso Escolar"] == "2022-23") & (df["Convocatoria"] == 1)]
    df["Título"] = df["Curso"]
    df["Curso"] = df[["Moodle_url", "Curso"]].apply(lambda x: f"[{x['Curso']}]({x['Moodle_url']})", axis=1)
    df['Categorías'] = df['Etiquetas']
    return df

df = get_data()

app.layout = html.Div([
        navbar,
        dbc.Row([
                dbc.Col([
                        dcc.Dropdown(df["Título"].unique(), id="titulo", placeholder="Selecciona un curso"),
                        html.Br(),
                        dcc.Dropdown(df["Categorías"].unique(), id="categoria", placeholder="Selecciona una categoría"),
                    ], width=6, style={"padding": "10px", "margin": "10px"}),
                dbc.Col([
                        html.Video(src="assets/videos/curso.mkv", controls=True, style={"width": "100%"}),
                    ], width=3, style={"padding": "10px", "margin": "10px"}),
                ], justify="center"),
        dbc.Row([       
            html.Br(),
            dbc.Col([], width=1),
            html.Div(id='output-table', style={"padding": "0px, 10px, 10px, 10px", "margin": "0px, 10px, 10px, 10px"}),
        ]),
        dbc.Row([       
            html.Br(),
        ])
])

@app.callback(
    Output(component_id='output-table', component_property='children'),
    # Output(component_id='titulo', component_property='value'), 
    # Output(component_id='categoria', component_property='value'), 
    Input(component_id='titulo', component_property='value'),
    Input(component_id='categoria', component_property='value'),
)
def update_output_div(titulo, categoria):
    """Filter dataframe by an unkown number of conditions"""
    df_copy = df.copy()
    if titulo:
        df_copy = df_copy[df_copy["Título"] == titulo]
    if categoria:
        df_copy = df_copy[df_copy["Categorías"] == categoria]
    return generate_table(df_copy) #, "", ""

if __name__ == '__main__':
    app.run_server(debug=False)