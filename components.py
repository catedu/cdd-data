import dash_bootstrap_components as dbc
from dash import dash_table, html

navbar = dbc.NavbarSimple(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src="assets/images/aularagon.png", height="50px"), width="12"),
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

def generate_table(df):
    tabla = dash_table.DataTable(
            df[["Curso","Categorías","Horas"]].join(df.filter(regex="\d\.\d").fillna("")).to_dict('records'), 
            [{"name": i, "id": i, "presentation": "markdown"} for i in df[["Curso","Categorías","Horas"]].join(df.filter(regex="\d\.\d")).columns],
            fixed_columns={ 'headers': True, 'data': 1 },
            # page_size=20,
            page_action="native",
            page_current= 0,
            page_size= 10,
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
                    'backgroundColor': '#F0EBD8',
                }
            ],
            style_header={
                'backgroundColor': '#748CAB',
                'color': 'white',
                # 'fontWeight': 'bold',
                # 'border': '1px solid black'
            },
            sort_action='native',
            fill_width=True,
            filter_action='native',
            filter_options={'case':'insensitive'},
            )
    return tabla

