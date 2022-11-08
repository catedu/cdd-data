from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pandas as pd

from components import navbar, generate_table
    

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

def get_data():
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-BAUvNUjp2AeV_daeeqHReX0M3ew3ZpEL3nfkrz96uUd816mV_hV1uWMvbsACphEBGjqHJBswGwFz/pub?gid=614465369&single=true&output=csv")
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
                        dcc.Dropdown(df["Título"].unique(), id="dropdown")
                    ], width=4,),
            ]),
        dbc.Row([       
            html.Br(),
            html.Div(id='my-output'),
        ])
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='dropdown', component_property='value')
)
def update_output_div(input_value):
    if input_value:
        return generate_table(df[df["Título"] == input_value])
    else:
        return generate_table(df)

if __name__ == '__main__':
    app.run_server(debug=True)