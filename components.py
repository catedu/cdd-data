import dash_bootstrap_components as dbc
from dash import dash_table

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

def generate_table(df):
    tabla = dash_table.DataTable(
            df[["Curso","Categorías","Horas"]].join(df.filter(regex="\d\.\d").fillna("")).to_dict('records'), 
            [{"name": i, "id": i, "presentation": "markdown"} for i in df[["Curso","Categorías","Horas"]].join(df.filter(regex="\d\.\d")).columns],
            fixed_columns={ 'headers': True, 'data': 1 },
            # page_size=20,
            page_action="native",
            page_current= 0,
            page_size= 20,
            style_table = {'minWidth': '100%'},
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['Curso', 'Categorías']
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold',
                'border': '1px solid black'
            },
            sort_action='native',
            )
    return tabla