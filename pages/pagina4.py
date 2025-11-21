import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime

dash.register_page(__name__, path='/pagina5', name='Covid-19')

layout = html.Div([
    html.Div([
        html.H2('Covid-19', className='title'),

        html.Div([
            html.Div([
                html.Label("Seleccione el país:"),
                dcc.Dropdown(
                    id='dropdown-pais',
                    options=[
                        {'label': 'Peru', 'value': 'Peru'},
                        {'label': 'Colombia', 'value': 'Colombia'},
                        {'label': 'Estados Unidos', 'value': 'USA'},
                        {'label': 'India', 'value': 'India'},
                        {'label': 'Brasil', 'value': 'Brazil'},
                    ],
                    value='Peru',
                    style={'width': '100%'},
                    className="input-field",
                ),
            ], className='input-group'),

            html.Div([
                html.Label("Dias historico"),
                dcc.Dropdown(
                    id='dropdown-dias-covid',
                    options=[
                        {'label': '30 dias', 'value': 30},
                        {'label': '60 dias', 'value': 60},
                        {'label': '90 dias', 'value': 90},
                        {'label': '120 dias', 'value': 120},
                        {'label': 'Todo el historico', 'value': 'all'},
                    ],
                    value=30,
                    style={'width': '100%'},
                    className="input-field",
                ),
            ], className='input-group'),

            html.Div(className='covid-actions', children=[
                html.Button('Actualizar Datos', id='btn-actualizar-covid', className='btn-generar'),
                html.Div(id='info-actualizado-covid')
            ]),

        ], className='covid-controls'),
    ], className='content left'),

    html.Div([
        html.H2('Estadisticas en Tiempo Real', className='title'),

        html.Div(className='covid-stats-grid', children=[
            html.Div(className='stat-card', children=[
                html.P('Total de Casos', className='stat-title'),
                html.P(id='total-casos', className='stat-value')
            ]),
            html.Div(className='stat-card', children=[
                html.P('Casos Nuevos', className='stat-title'),
                html.P(id='casos-nuevos', className='stat-value')
            ]),
            html.Div(className='stat-card', children=[
                html.P('Total de Muertes', className='stat-title'),
                html.P(id='total-muertes', className='stat-value')
            ]),
            html.Div(className='stat-card', children=[
                html.P('Recuperados', className='stat-title'),
                html.P(id='total-recuperados', className='stat-value')
            ]),
        ]),

        html.Div(className='covid-graph-container', children=[
            dcc.Graph(id='grafica-covid', style={'height': '470px', 'width': '100%'}, config={'displayModeBar': True}, responsive=True)
        ])

    ], className='content right'),

], className='page-container')

#### FUNCIONES PARA CONECTAR A LA API #####
def obtener_datos_pais(pais):
    try: 
        url = f"https://disease.sh/v3/covid-19/countries/{pais}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos para {pais}: {e}")
        return None
    
def obtener_historico_pais(pais, dias):
    try:
        url = f"https://disease.sh/v3/covid-19/historical/{pais}"
        params = {'lastdays': dias}
        response = requests.get(url, params=params ,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener historico para {pais}: {e}")
        return None
    
def formatear_numero(numero): #150000 -> 150,000
    if numero is None:
        return "N/A"
    return f"{numero:,}"   

#### CALLBACKS ####
@callback(
    Output('total-casos', 'children'),
    Output('casos-nuevos', 'children'),
    Output('total-muertes', 'children'),
    Output('total-recuperados', 'children'),
    Output('grafica-covid', 'figure'),
    Output('info-actualizado-covid', 'children'),
    Input('btn-actualizar-covid', 'n_clicks'),
    State('dropdown-pais', 'value'),
    State('dropdown-dias-covid', 'value'),
    prevent_initial_call=False
)

def actualizar_dashboard_covid(n_clicks, pais, dias): 
    datos_actuales = obtener_datos_pais(pais)
    historico = obtener_historico_pais(pais, dias)

    if not datos_actuales or not historico:
        fig = go.Figure()
        fig.add_annotation(
            text="Error al obtener datos", 
            xref="paper", 
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=15, color="red")
            )
        fig.update_layout(
            paper_bgcolor='lightcyan',
            plot_bgcolor='white'
        )

        return "N/A", "N/A", "N/A", "N/A", fig, "No se pudieron actualizar los datos."
    
    total_casos = datos_actuales.get('cases', 0)
    casos_hoy = datos_actuales.get('todayCases', 0)
    total_muertes = datos_actuales.get('deaths', 0)
    total_recuperados = datos_actuales.get('recovered', 0)

    total_casos_texto = formatear_numero(total_casos)
    casos_hoy_texto = formatear_numero(casos_hoy)
    total_muertes_texto = formatear_numero(total_muertes)
    total_recuperados_texto = formatear_numero(total_recuperados)

    timeline = historico.get('timeline', {})
    casos_historico = timeline.get('cases', {})
    muertes_historicas = timeline.get('deaths', {})

    fechas = list(casos_historico.keys())
    valores_casos = list(casos_historico.values())
    valores_muertes = list(muertes_historicas.values())

    fechas_dt = [datetime.strptime(fecha, '%m/%d/%y') for fecha in fechas]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_casos,
        mode='lines',
        fill='tozeroy',
        name='Casos Totales',
        line=dict(color='yellow', width=2),
        marker=dict(size=6, color='yellow'),
        hovertemplate='Fecha: %{x|%Y-%m-%d}<br>Casos: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_muertes,
        mode='lines',
        name='Muertes Totales',
        line=dict(color='red', width=2),
        marker=dict(size=6, color='red'),
        hovertemplate='Fecha: %{x|%Y-%m-%d}<br>Muertes: %{y}<extra></extra>'
    ))

    return (total_casos_texto, casos_hoy_texto, total_muertes_texto,
            total_recuperados_texto, fig,
            f"Datos actualizados para {pais}.")
