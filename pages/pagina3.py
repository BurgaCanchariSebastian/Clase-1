import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path='/pagina4', name='Modelo SIR')

layout = html.Div([
    html.Div([
        html.H2('Modelo SIR - Epidemologia', className='title'),

        html.Div([
            html.Label("Población Total (N):"),
            dcc.Input(id='input-N', type='number', value=1000, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Tasa de transmision (β):"),
            dcc.Input(id='input-beta', type='number', value=0.3, step=0.01, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Tasa de recuperación (γ):"),
            dcc.Input(id='input-gamma', type='number', value=0.1, step=0.01, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Infectados iniciales (I0):"),
            dcc.Input(id='input-I0', type='number', value=1, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Tiempo de simulación:"),
            dcc.Input(id='input-tiempo', type='number', value=100, className="input-field"),
        ], className='input-group'),

        html.Button('Simular Epidemia', id='btn-simular', className='btn-generar'),
    ], className='content left'),

    html.Div([
        html.H2('Evolucion de la Epidemia', className='title'),
        dcc.Graph(id='grafica-sir', style={'height': '470px'}, config={'displayModeBar': True}, responsive=True),
    ], className='content right'),
],className='page-container')


#Modelo SIR
def modelo_sir(y, t , beta, gamma, N):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

#### Callback ###
@callback(
    Output('grafica-sir', 'figure'),
    Input('btn-simular', 'n_clicks'),
    State('input-N', 'value'),
    State('input-beta', 'value'),
    State('input-gamma', 'value'),
    State('input-I0', 'value'),
    State('input-tiempo', 'value'),
    prevent_initial_call=False
)

def simular_epidemia(n_clicks, N, beta, gamma, I0, tiempo_max):
    S0 = N - I0
    R0_inicial = 0
    y0 = [S0, I0, R0_inicial]

    t = np.linspace(0, tiempo_max, 200)

    try:
        solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, N))
        S, I, R = solucion.T
    except Exception as e:
        S = np.full_like(t, S0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0_inicial)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S,
          mode='lines', 
          name='Susceptibles (S)', 
          line=dict(color='blue', width=2),
          hovertemplate='Dia: %{x:.0f}<br>Susceptibles: %{y:.0f}<extra></extra>',
          ))
    fig.add_trace(go.Scatter(
        x=t, y=I
        , mode='lines', 
        name='Infectados (I)', 
        line=dict(color='red'),
        hovertemplate='Dia: %{x:.0f}<br>Infectados: %{y:.0f}<extra></extra>',
        ))
    fig.add_trace(go.Scatter(
        x=t, y=R, 
        mode='lines', 
        name='Recuperados (R)', 
        line=dict(color='green'),
        hovertemplate='Dia: %{x:.0f}<br>Recuperados: %{y:.0f}<extra></extra>',
        ))
    
    fig.update_layout(
        title=dict(
            text='<b>Evolución del Modelo SIR</b>',
            font=dict(size=16, color='darkred'),
            x=0.5,
        ),
        xaxis_title='Tiempo (días)',
    yaxis_title='Número de Personas',
        paper_bgcolor='lightyellow',
    plot_bgcolor='white',
    font=dict(family='Outfit', size=12, color='black'),
        legend=dict(
            orientation="h", yanchor="bottom", y=0.999,
            xanchor="center", x=0.5
        ),
        margin=dict(l=20, r=40, t=80, b=40),
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='black',
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='black',
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
    )

    return fig

        

    