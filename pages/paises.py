from dash import html, dcc, callback, Input, Output, State, exceptions as _dash_exceptions
import dash
import requests
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta


# Register the page (safe to ignore PageError if imported outside app context)
_PAGE_REGISTERED = False
try:
    dash.register_page(__name__, path='/climas', name='Climas')
    _PAGE_REGISTERED = True
except _dash_exceptions.PageError:
    _PAGE_REGISTERED = False


CITY_OPTIONS = {
    'Lima,PE': {'lat': -12.0464, 'lon': -77.0428},
    'Madrid,ES': {'lat': 40.4168, 'lon': -3.7038},
    'Londres,GB': {'lat': 51.5074, 'lon': -0.1278},
    'Nueva York,US': {'lat': 40.7128, 'lon': -74.0060},
    'Tokio,JP': {'lat': 35.6895, 'lon': 139.6917},
}


layout = html.Div([
    html.Div([
        html.H2('Clima - Pronóstico', className='title'),

        html.Div([
            html.Label('Ciudad:'),
            dcc.Dropdown(id='dropdown-ciudad', options=[{'label': k, 'value': k} for k in CITY_OPTIONS.keys()], value='Lima,PE', className='input-field'),
        ], className='input-group'),

        html.Div([
            html.Label('Horizonte (días):'),
            dcc.Dropdown(id='dropdown-dias-clima', options=[{'label': str(x), 'value': x} for x in [1,3,7,10,14]], value=7, className='input-field'),
        ], className='input-group'),

        html.Div(className='covid-actions', children=[
            html.Button('Actualizar Clima', id='btn-actualizar-clima', className='btn-generar'),
            html.Div(id='info-actualizado-clima')
        ]),

    ], className='content left'),

    html.Div([
        html.H2('Resumen y Gráfica', className='title'),

        html.Div(className='covid-stats-grid', children=[
            html.Div(className='stat-card', children=[html.P('Temperatura (°C)', className='stat-title'), html.P(id='clima-temp-current', className='stat-value')]),
            html.Div(className='stat-card', children=[html.P('Viento (m/s)', className='stat-title'), html.P(id='clima-wind', className='stat-value')]),
            html.Div(className='stat-card', children=[html.P('Precipitación (mm)', className='stat-title'), html.P(id='clima-precip', className='stat-value')]),
            html.Div(className='stat-card', children=[html.P('Humedad (%)', className='stat-title'), html.P(id='clima-humidity', className='stat-value')]),
        ]),

        html.Div(className='covid-graph-container', children=[
            dcc.Graph(id='grafica-clima', style={'height': '470px', 'width': '100%'}, config={'displayModeBar': True}, responsive=True)
        ])

    ], className='content right'),

], className='page-container')


def fetch_weather(lat, lon, days):
    """Fetch forecast weather using Open-Meteo (no API key required). Returns JSON or None."""
    try:
        url = (
            'https://api.open-meteo.com/v1/forecast'
            f'?latitude={lat}&longitude={lon}'
            '&hourly=temperature_2m,relativehumidity_2m,precipitation,wind_speed_10m'
            '&current_weather=true'
            f'&forecast_days={int(days)}&timezone=auto'
        )
        resp = requests.get(url, timeout=12)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def format_number(n, digits=1):
    try:
        if n is None:
            return 'N/A'
        if isinstance(n, (int, float)):
            if abs(n) >= 1000:
                return f"{n:,.{digits}f}"
            return f"{n:.{digits}f}"
        return str(n)
    except Exception:
        return str(n)


@callback(
    Output('clima-temp-current', 'children'),
    Output('clima-wind', 'children'),
    Output('clima-precip', 'children'),
    Output('clima-humidity', 'children'),
    Output('grafica-clima', 'figure'),
    Output('info-actualizado-clima', 'children'),
    Input('btn-actualizar-clima', 'n_clicks'),
    State('dropdown-ciudad', 'value'),
    State('dropdown-dias-clima', 'value'),
    prevent_initial_call=False
)
def actualizar_clima(n_clicks, ciudad, dias):
    info_msg = ''
    opt = CITY_OPTIONS.get(ciudad)
    if not opt:
        fig = go.Figure()
        return 'N/A', 'N/A', 'N/A', 'N/A', fig, 'Ciudad no encontrada.'

    data = fetch_weather(opt['lat'], opt['lon'], dias)
    if not data:
        fig = go.Figure()
        return 'N/A', 'N/A', 'N/A', 'N/A', fig, 'Error al obtener datos del servicio de clima.'

    # current weather
    current = data.get('current_weather', {})
    temp = current.get('temperature')
    wind = current.get('windspeed')

    # hourly
    hourly = data.get('hourly', {})
    times = hourly.get('time', [])
    temps = hourly.get('temperature_2m', [])
    precip = hourly.get('precipitation', [])
    humidity = hourly.get('relativehumidity_2m', [])

    # Build dataframe for plotting
    try:
        df = pd.DataFrame({'time': times, 'temperature': temps, 'precipitation': precip, 'humidity': humidity})
        df['time'] = pd.to_datetime(df['time'])
    except Exception:
        df = pd.DataFrame()

    # Stats aggregation
    total_precip = float(df['precipitation'].sum()) if not df.empty else None
    avg_humidity = float(df['humidity'].mean()) if not df.empty else None

    # figure
    fig = go.Figure()
    if not df.empty:
        fig.add_trace(go.Scatter(x=df['time'], y=df['temperature'], mode='lines', name='Temp (°C)', line=dict(color='red')))
        fig.update_layout(xaxis_title='Fecha', yaxis_title='Temperatura (°C)')
    else:
        fig.add_annotation(text='No hay datos horarios', xref='paper', yref='paper', x=0.5, y=0.5, showarrow=False)

    return (
        format_number(temp, 1) + ' °C' if temp is not None else 'N/A',
        format_number(wind, 1) + ' m/s' if wind is not None else 'N/A',
        format_number(total_precip, 1) + ' mm' if total_precip is not None else 'N/A',
        format_number(avg_humidity, 0) + ' %' if avg_humidity is not None else 'N/A',
        fig,
        f'Datos actualizados para {ciudad}'
    )
