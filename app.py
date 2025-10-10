import dash
from dash import html
import dash_bootstrap_components as dbc
import plotly.io as pio

external_stylesheets = [dbc.themes.LUX, '/assets/css/style.css']
pio.templates.default = "plotly_dark"

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)
server = app.server

ordered_names = ["Inicio", "Página 1", "Página 2"]
pages = list(dash.page_registry.values())
pages.sort(key=lambda p: ordered_names.index(p["name"]) if p["name"] in ordered_names else 99)

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Técnicas de Modelamiento Matemático", className="fw-bold fs-3 text-white"),
            dbc.Nav([dbc.NavItem(dbc.NavLink(p["name"], href=p["relative_path"], active="exact",
                                              className="text-white")) for p in pages],
                    pills=True, className="ms-auto")
        ]),
        color="primary", dark=True, className="mb-4 shadow-lg rounded-bottom"
    ),

    
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(dash.page_container),
                    className="w-100 shadow-lg rounded-4",
                    style={"maxWidth": "1500px"}  
                ),
                xs=12, className="mx-auto d-flex justify-content-center"
            )
        ], className="g-0 py-3")
    ], fluid=True, className="p-0")
])

if __name__ == "__main__":
    app.run(debug=True)  
