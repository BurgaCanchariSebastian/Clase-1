import dash
from dash import html, dcc

app = dash.Dash(__name__, use_pages=True)

ordered_names = ["Inicio", "Página 1", "Página 2"]
pages = list(dash.page_registry.values())
pages.sort(key=lambda page: ordered_names.index(page['name']) if page['name'] in ordered_names else 99)

app.layout = html.Div([
    html.H1("Tecnicas de Modelamiento Matemático", className='app-header'),
    html.Div([
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']}", href=page["relative_path"], className='nav-link'),
            ) for page in dash.page_registry.values()
        ], className='nav-links')
    ], className='navegation'),
    dash.page_container
], className='app.container')

if __name__ == '__main__':      
    app.run(debug=True)