import dash 
from dash import html, dcc

dash.register_page(__name__, path='/pagina2', name='Pagina2')

layout = html.Div([
    html.H3('Bienvenido a la página 2'),
])