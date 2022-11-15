import dash_bootstrap_components as dbc
from dash import dash_table, html, dcc
from data import number_of_input_rows

NIVEL_DE_PROGRESION = [
    "Conocimiento teórico",
    "Uso guiado",
    "Uso autónomo",
    "Aplicación en el aula",
]


def generate_table(df):
    tabla = dash_table.DataTable(
        df[["Curso", "Categorías", "Horas"]]
        .join(df.filter(regex="\d\.\d").fillna(""))
        .to_dict("records"),
        [
            {"name": i, "id": i, "presentation": "markdown"}
            for i in df[["Curso", "Categorías", "Horas"]]
            .join(df.filter(regex="\d\.\d"))
            .columns
        ],
        fixed_columns={"headers": True, "data": 1},
        # page_size=20,
        page_action="native",
        page_current=0,
        page_size=10,
        style_table={"minWidth": "100%"},
        style_cell_conditional=[
            {"if": {"column_id": c}, "textAlign": "left"}
            for c in ["Curso", "Categorías"]
        ],
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#F0EBD8",
            }
        ],
        style_header={
            "backgroundColor": "#748CAB",
            "color": "white",
            # 'fontWeight': 'bold',
            # 'border': '1px solid black'
        },
        sort_action="native",
        fill_width=True,
        filter_action="native",
        filter_options={"case": "insensitive"},
    )
    return tabla


def generate_filtered_table(df):
    # TODO: Hacer tablas de participante, coordinador, tutor.
    ## Coordinador todo igual que participante menos Área 1 = todo B1
    ## Tutor: todas las competencias que vengan rellenadas a C1
    area_colors = {
        1: "#F0EBD8",
        2: "green",
        3: "#F0EBD8",
        4: "#F0EBD8",
        5: "#F0EBD8",
        6: "#F0EBD8",
    }

    def generate_area_table(df, numero_area):
        df_copy = df.filter(regex=f"{numero_area}\.\d")
        tabla = html.Table(
            # Header
            [html.Tr([html.Th(col) for col in df_copy.columns])] +
            # Body
            [
                html.Tr([html.Td(df_copy.iloc[i][col]) for col in df_copy.columns])
                for i in range(len(df_copy))
            ],
            style={
                "width": "100%",
                "border": "1px solid black",
                "background": area_colors[numero_area],
            },
        )
        return tabla

    tablas = [generate_area_table(df, i) for i in range(1, 7)]

    return tablas


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
    color="#5EC877",
    dark=False,
)

# TODO: Si se ha trabajado la actividad con alumnado y
# se demuestra que han alcanzado el nivel de progresión
# se mapea el área 6 con lo que venga, si no se borra
actividad_con_alumnado = dbc.Switch(
    id="bool-con-alumnado",
    label="¿Adquiere esta competencia el alumnado?",
    value=False,
)

# Por debajo de 10 horas la puntuación máxima es un A2 ¿Máximo de horas?
horas = dbc.Input(
    id="n-horas",
    type="number",
    placeholder="Introduce el número horas",
    min=0,
    max=100,
    step=10,
    style={"margin": "10px", "margin-right": "30px"},
)


modalidad = dcc.Dropdown(
    [
        {"label": item, "value": i + 1}
        for i, item in enumerate(["Presencial", "Online", "Mixto", "Grupo de trabajo"])
    ],
    id="modalidad",
    placeholder="Selecciona la modalidad",
    style={"margin": "10px", "margin-right": "30px"},
)

###############

input_group = dbc.Input(
    id=f"palabras-clave",
    type="text",
    placeholder="Introduce palabras clave separadas por comas",
    style={"margin": "10px", "margin-right": "30px"},
)

###############

search_inputs_rows = [
    dbc.Row(
        [
            dbc.Col(
                [
                    horas,
                ],
                lg=3,
                md=4,
                xs=12,
            ),
            dbc.Col(
                [
                    modalidad,
                ],
                lg=3,
                md=4,
                xs=12,
            ),
            dbc.Col(
                [
                    actividad_con_alumnado,
                ],
                lg=3,
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
                    # TODO: meter una data table con las competencias
                    input_group,
                ],
                lg=3,
                md=4,
                xs=12,
            ),
        ],
        justify="center",
        style={"margin": "10px"},
    ),
]
