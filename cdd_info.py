from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from components import generate_filtered_table, search_inputs_rows, navbar

# Create this dict as an ordered dict
int_competencias = {
    1: "A1",
    2: "A2",
    3: "B1",
    4: "B2",
    5: "C1",
    6: "C2",
}


def convert_int_to_competencias(df):
    df.iloc[:, -23:] = (
        df.filter(regex="\d\.\d")
        .fillna(0)
        .astype(int)
        .applymap(int_competencias.get)
        .fillna("")
    )
    return df


app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

server = app.server

df = pd.read_csv("Dicc.csv", sep=";")


df["bag_of_words"] = (
    df[["PALABRA_CLAVE", "SINONIMOS"]]
    .fillna("")
    .apply(lambda x: x[0].lower().split(",") + x[1].lower().split(","), axis=1)
)
df["bag_of_words"] = df["bag_of_words"].apply(lambda x: [x.strip() for x in x])

app.layout = html.Div(
    [navbar] +
    search_inputs_rows + 
    [
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
    Input("palabra-clave", "value"),
)
def show_table(palabra_clave):
    if palabra_clave is None or palabra_clave.strip() == "":
        return None
    palabra_clave = palabra_clave.strip().lower()
    df_filtered = df.loc[
        df["bag_of_words"].apply(lambda x: palabra_clave in x),
        df.filter(regex="\d\.\d").columns,
    ]
    df_filtered = convert_int_to_competencias(df_filtered)
    return generate_filtered_table(df_filtered)


if __name__ == "__main__":
    df
    app.run_server(debug=True)
