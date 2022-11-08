from dash import Dash, dash_table, html
import pandas as pd

app = Dash(__name__)

#Markdown format for image as a link: [![alt text](image link)](web link)
seattle = "[![Seattle](https://upload.wikimedia.org/wikipedia/commons/8/80/SeattleQueenAnne2021-2.png#thumbnail)](https://en.wikipedia.org/wiki/Seattle)"
montreal = "[![Montreal](https://upload.wikimedia.org/wikipedia/commons/d/d0/Montreal_August_2017_05.jpg#thumbnail)](https://en.wikipedia.org/wiki/Montreal)"
nyc = "[![New York City](https://upload.wikimedia.org/wikipedia/commons/f/f7/Lower_Manhattan_skyline_-_June_2017.jpg#thumbnail)](https://en.wikipedia.org/wiki/New_York_City)"

"""

Use css in the assets folder to set the image size, for example:

img[src*="#thumbnail"] {
   width:200px;
   height:100px;
}
"""




df = pd.DataFrame(
    dict(
        [
            ("temperature", [13, 43, 50]),
            ("city", ["NYC", "Montreal", "Seattle"]),
            ("image", [nyc, montreal, seattle]),
        ]
    )
)

app.layout = html.Div(
    [
        dash_table.DataTable(
            id="table-dropdown",
            data=df.to_dict("records"),
            columns=[
                {"id": "image", "name": "image", "presentation": "markdown"},
                {"id": "city", "name": "city"},
                {"id": "temperature", "name": "temperature"},
            ],
            style_cell_conditional=[{"if": {"column_id": "image"}, "width": "200px"},],
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)