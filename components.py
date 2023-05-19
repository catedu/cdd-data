import dash_bootstrap_components as dbc
from dash import dash_table, html, dcc
from slugify import slugify


from data import input_df, NIVEL_DE_PROGRESION
PLOTLY_LOGO = "https://educa.aragon.es/o/educaragon-theme/images/header/banda.png"
PLOTLY_Trans = "https://www.cddaragon.es/wp-content/uploads/2022/06/CARAMELO-BISEL-logocabecera.png"

def generate_bootstrap_table(df, nombres_competencias):
    def get_name(key):
        for dictionary in nombres_competencias:
            if key in dictionary:
                return dictionary[key]
        return None 
    
    header = [
        html.Th(name, id=f"{slugify(name)}", key=f"{slugify(name)}") 
        for name in df.columns
    ]
    
    body = [
        html.Tr([
            html.Td(df.iloc[i][col]) 
            for col in df.columns
        ]) 
        for i in range(len(df))
    ]
    
    tooltips = [
        dbc.Tooltip(get_name(name), target=f"{slugify(name)}") 
        for name in df.columns
    ]
    
    table = dbc.Table(
        # Use the children property to add each row
        children=[
            html.Thead(html.Tr(header)),
            html.Tbody(body),
        ] + tooltips,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        style={"margin": "20px", "width": "96%", "background-color":"white"},
    )
    return table

navbar = dbc.Navbar(
    dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Pre-mapeo de Formación con CDD", className="ms-2", style={"color":"white"})),
                        ],
                        align="left",
                        className="g-0",
                    ),
                    href="https://plotly.com",
                    style={"textDecoration": "none", "margin-left":"-100px"},
                ),

            ]
        ),
    color="dark",
    dark=True
)


# Si se ha trabajado la actividad con alumnado y
# se demuestra que han alcanzado el nivel de progresión
# se mapea el área 6 con lo que venga, si no se borra
actividad_con_alumnado = dbc.Switch(
    id="bool-con-alumnado",
    label="Se concreta cómo enseñar estas Competencias Digitales al alumnado.",
    value=False,
    style={"margin": "10px", "margin-top":"20px"},
)

# Por debajo de 10 horas la puntuación máxima es un A2 ¿Máximo de horas?
horas = dbc.Switch(
                    id="menos-de-10-horas",
                    label="La actividad tiene menos de 10 horas.",
                    value=False,
                    style={"margin": "10px", "margin-top": "20px"},
)


modalidad = dcc.Dropdown(
    [
        {"label": item, "value": i + 1}
        for i, item in enumerate(["Presencial", "Online", "Mixto", "Grupo de trabajo"])
    ],
    id="modalidad",
    placeholder="Selecciona la modalidad",
    style = {"margin-top": "10px","margin-bottom":"10px", "margin-right": "30px", "background-color":"#E8E8E8", "width":"280px"}
)

# TODO: Cambiar el text area por un input https://community.plotly.com/t/auto-complete-text-suggestion-option-in-textfield/8940/6
# para que añada elementos seleccionados debajo del campo de texto
palabras_clave = dbc.Textarea(
    id="palabras-clave",
    size="sm",
    placeholder="Introduce herramientas/plataformas/Apps que formen parte de los contenidos de la formación; separado por comas ( , )",
    style={"margin-top": "10px", "margin-bottom": "10px", "margin-right": "30px", "background-color": "#E8E8E8"}
)

palabras_no_encontradas = html.Div(id="no-encontrado", style={"margin-top":"2px","margin-bottom":"20px","color":"#FF6060"})

search_inputs_rows = [

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
                            "minWidth": "190px",
                            "width": "190px",
                            "maxWidth": "190px",
                            "whiteSpace": "normal",
                            "textAlign": "left",
                            "fontFamily":"Helvetica",
                        },
                        style_header = {
                            "fontWeight":"bold",
                            "backgroundColor":"#E8E8E8",
                            "textAlign": "center",
                            "fontFamily":"Helvetica",

                        },
                        style_cell_conditional=[
                            {'if': {'column_id': 'nivel-de-progresion'},
                             'width': '30%'},
                        ]
                    ),

                    dbc.Button("Añadir fila",
                               id="editing-rows-button",
                               n_clicks=0,
                               size="sm",
                               style={"margin-top":"20px","background-color":"black"}),
                    dbc.Button(
                        "Actualizar datos del csv",
                        id="refresh-data",
                        size="sm",
                        style={"margin-left": "30px", "margin-right": "10px", "margin-top":"20px","background-color":"black"},
                    ),
                    html.Div(id="output-last-update", style={"padding-top":"1%","font-size":"12px", "margin-left":"130px"}),
                ],
                lg=8,
                md=8,
                xs=12,
            ),
        ],
        justify="left",
        style={"margin": "20px","padding-top":"1%"},
    ),
#Row de palabrqas clave
dbc.Row(
        [
            dbc.Col(
                [
                    palabras_clave,
                    palabras_no_encontradas,
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
        justify="left",
        style={"margin": "20px"},
    ),
]