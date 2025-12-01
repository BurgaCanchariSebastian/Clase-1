import dash
from dash import html, dcc, callback, Input, Output, State, exceptions as _dash_exceptions
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint


_PAGE_REGISTERED = False
try:
    dash.register_page(__name__, path='/pagina_seir', name='Modelo SEIR')
    _PAGE_REGISTERED = True
except _dash_exceptions.PageError:
    # Se intenta registrar fuera del contexto de la app (p. ej. import directo para pruebas).
    # No abortamos la importación: permitimos que el módulo se importe sin registrar la página.
    _PAGE_REGISTERED = False


def register_page_if_possible():
    """Intentar registrar la página de nuevo. Llamar desde el módulo principal después
    de crear la instancia de la app si fuese necesario (por ejemplo, desde `app.py`).
    """
    global _PAGE_REGISTERED
    if _PAGE_REGISTERED:
        return True
    try:
        dash.register_page(__name__, path='/pagina_seir', name='Modelo SEIR')
        _PAGE_REGISTERED = True
        return True
    except Exception:
        return False


layout = html.Div([
    html.Div([
        html.H2('Modelo SEIR - Epidemiología', className='title'),

        html.Div([
            html.Label("Población Total (N):"),
            dcc.Input(id='seir-input-N', type='number', value=10000, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Tasa de transmisión (β):"),
            dcc.Input(id='seir-input-beta', type='number', value=0.5, step=0.01, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Tasa de incubación (σ) [1/días]:"),
            dcc.Input(id='seir-input-sigma', type='number', value=1/5.2, step=0.01, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Tasa de recuperación (γ):"),
            dcc.Input(id='seir-input-gamma', type='number', value=0.1, step=0.01, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Expuestos iniciales (E0):"),
            dcc.Input(id='seir-input-E0', type='number', value=0, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Infectados iniciales (I0):"),
            dcc.Input(id='seir-input-I0', type='number', value=1, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Tiempo de simulación (días):"),
            dcc.Input(id='seir-input-tiempo', type='number', value=160, className="input-field"),
        ], className='input-group'),

        html.Button('Simular SEIR', id='btn-simular-seir', className='btn-generar'),
    ], className='content left'),

    html.Div([
        html.H2('Evolución del Modelo SEIR', className='title'),
        dcc.Graph(id='grafica-seir', style={'height': '520px'}, config={'displayModeBar': True}, responsive=True),
    ], className='content right'),
], className='page-container')


def modelo_seir(y, t, beta, sigma, gamma, N):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]


@callback(
    Output('grafica-seir', 'figure'),
    Input('btn-simular-seir', 'n_clicks'),
    State('seir-input-N', 'value'),
    State('seir-input-beta', 'value'),
    State('seir-input-sigma', 'value'),
    State('seir-input-gamma', 'value'),
    State('seir-input-E0', 'value'),
    State('seir-input-I0', 'value'),
    State('seir-input-tiempo', 'value'),
    prevent_initial_call=False
)
def simular_seir(n_clicks, N, beta, sigma, gamma, E0, I0, tiempo_max):
    # Validate and set defaults
    try:
        N = float(N) if N is not None else 10000.0
        beta = float(beta) if beta is not None else 0.5
        sigma = float(sigma) if sigma is not None else 1/5.2
        gamma = float(gamma) if gamma is not None else 0.1
        E0 = float(E0) if E0 is not None else 0.0
        I0 = float(I0) if I0 is not None else 1.0
        tiempo_max = float(tiempo_max) if tiempo_max is not None else 160.0
    except Exception:
        # Fallback defaults
        N, beta, sigma, gamma, E0, I0, tiempo_max = 10000.0, 0.5, 1/5.2, 0.1, 0.0, 1.0, 160.0

    S0 = N - E0 - I0
    R0 = 0.0
    y0 = [S0, E0, I0, R0]

    t = np.linspace(0, tiempo_max, 400)

    try:
        sol = odeint(modelo_seir, y0, t, args=(beta, sigma, gamma, N))
        S, E, I, R = sol.T
    except Exception:
        S = np.full_like(t, S0)
        E = np.full_like(t, E0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=t, y=E, mode='lines', name='Expuestos (E)', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='green')))

    fig.update_layout(
        title=dict(text='<b>Evolución del Modelo SEIR</b>', font=dict(size=16, color='darkred'), x=0.5),
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de Personas',
        paper_bgcolor='lightyellow',
        plot_bgcolor='white',
        font=dict(family='Outfit', size=12, color='black'),
        legend=dict(orientation='h', yanchor='bottom', y=0.99, xanchor='center', x=0.5),
        margin=dict(l=20, r=40, t=80, b=40),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='black', zeroline=True, zerolinewidth=2, zerolinecolor='black')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black', zeroline=True, zerolinewidth=2, zerolinecolor='black')

    return fig
