import dash_bootstrap_components as dbc
from dash import dash_table, html, dcc
from slugify import slugify

from data import input_df, NIVEL_DE_PROGRESION


def generate_bootstrap_table(df):
    return dbc.Table.from_dataframe(
        df,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        style={"margin": "20px", "width": "96%"},
    )


navbar = dbc.NavbarSimple(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src="assets/images/aularagon.png", height="50px"),
                        width="12",
                    ),
                ],
                align="left",
            ),
            href="https://moodle.catedu.es",
            # style={"textDecoration": "none"},
        ),
    ],
    color="primary",  # "#5EC877",
    dark=False,
)

# TODO: Si se ha trabajado la actividad con alumnado y
# se demuestra que han alcanzado el nivel de progresión
# se mapea el área 6 con lo que venga, si no se borra
actividad_con_alumnado = dbc.Switch(
    id="bool-con-alumnado",
    label="¿Adquiere esta competencia el alumnado?",
    value=False,
    style={"margin": "10px", "margin-right": "30px"},
)

# Por debajo de 10 horas la puntuación máxima es un A2 ¿Máximo de horas?
horas = dbc.Switch(
    id="menos-de-10-horas",
    label="¿El curso tiene menos de 10 horas?",
    value=False,
    style={"margin": "10px", "margin-right": "30px"},
)


modalidad = dcc.Dropdown(
    [
        {"label": item, "value": i + 1}
        for i, item in enumerate(["Presencial", "Online", "Mixto", "Grupo de trabajo"])
    ],
    id="modalidad",
    placeholder="Selecciona la modalidad",
    style={"margin": "10px", "margin-top": "30px"},
)

palabras_clave = dbc.Textarea(
    id="palabras-clave",
    size="sm",
    placeholder="Introduce palabras clave separadas por comas",
    style={"margin": "10px", "margin-right": "30px"},
)

search_inputs_rows = [
    dbc.Row(
        [
            dbc.Col(
                [
                    palabras_clave,
                    modalidad,
                ],
                lg=8,
                md=8,
                xs=12,
            ),
            dbc.Col(
                [
                    actividad_con_alumnado,
                    horas,
                ],
                lg=4,
                md=4,
                xs=12,
            ),
        ],
        justify="center",
        style={"margin": "10px"},
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    dash_table.DataTable(
                        id="adding-rows-table",
                        columns=[
                            {"name": i, "id": slugify(i), "presentation": "dropdown"}
                            for i in input_df.columns
                        ],
                        data=input_df[:2].to_dict("records"),
                        editable=True,
                        row_deletable=True,
                        dropdown={
                            "competencias": {
                                "options": [
                                    {"label": i, "value": i}
                                    for i in input_df["Competencias"].unique()
                                ],
                            },
                            "nivel-de-progresion": {
                                "options": [
                                    {"label": i, "value": i}
                                    for i in input_df["Nivel de progresión"]
                                ]
                            },
                        },
                        # style_table={'overflowX': 'auto'},
                        style_cell={
                            "height": "auto",
                            # all three widths are needed
                            "minWidth": "180px",
                            "width": "180px",
                            "maxWidth": "180px",
                            "whiteSpace": "normal",
                            "textAlign": "left",
                        },
                    ),
                    dbc.Button("Add Row", id="editing-rows-button", n_clicks=0),
                ],
                lg=8,
                md=8,
                xs=12,
            ),
        ],
        justify="center",
        style={"margin": "10px"},
    ),
]
