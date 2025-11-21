import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path='/pagina3', name='Campo Vectorial')

layout = html.Div([
    html.Div([
        html.H2('Campo Vectorial 2D', className='title'),

        html.Div([
            html.Label("Ecuacion dx/dt = "),
            dcc.Input(id='input-fx', type='text', value='np.sin(x)', className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Ecuacion dy/dt = "),
            dcc.Input(id='input-fy', type='text', value='np.cos(x)', className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Rango del Eje X:"),
            dcc.Input(id='input-xmax', type='number', value=5, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Rango del Eje Y:"),
            dcc.Input(id='input-ymax', type='number', value=5, className="input-field"),
        ], className='input-group'),

        html.Div([
            html.Label("Mallado"),
            dcc.Input(id='input-n', type='number', value=15, className="input-field"),
        ], className='input-group'),

        html.Button('Generar Campo Vectorial', id='btn-generate', className='btn-generar'),

        #Ejemplos
        html.Div([
            html.H3("Ejemplos de Ecuaciones:"),
            html.Ul([
                html.Li("dx/dt = y , dy/dt = -x  (Movimiento Circular)"),
                html.Li("dx/dt = x , dy/dt = y  (Crecimiento Exponencial)"),
                html.Li("dx/dt = -y , dy/dt = x  (Movimiento Circular Inverso)"),
                html.Li("dx/dt = x - y , dy/dt = x + y  (Combinación Lineal)"),
            ])
        ], className='examples-container'),
    ], className='content left'),

    html.Div([
        html.H2('Visualización del Campo Vectorial', className='title'),
        dcc.Graph(id='vector-field-graph', style={'height': '470px'}, config={'displayModeBar': True}, responsive=True),

        html.Div(id='info-campo')
    ], className='content right'),
],className='page-container')

#### Callback #### 
@callback(
    [Output("vector-field-graph", "figure"),
    Output("info-campo", "children")],
    Input("btn-generate", "n_clicks"),
    State("input-fx", "value"),
    State("input-fy", "value"),
    State("input-xmax", "value"),
    State("input-ymax", "value"),
    State("input-n", "value"),
    prevent_initial_call=False
)
def graficar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    info_mensaje = ""
    try:
       diccionario = {
            'X': X,
            'Y': Y,
            'x': X,
            'y': Y,
            'np': np,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': np.exp,
            'pi': np.pi,
            'e': np.e,
            'log': np.log,
       }

       # Evaluar las funciones en el contexto controlado
       fx = eval(fx_str, {}, diccionario)
       fy = eval(fy_str, {}, diccionario)

       mag = np.sqrt(fx**2 + fy**2)
       mag_max = np.max(mag)
       mag_min = np.min(mag)
       info_mensaje = f"Magnitud Máxima: {mag_max:.2f} | Magnitud Mínima: {mag_min:.2f}"
    except Exception as error:
       # En caso de error, usar vectores nulos y mostrar mensaje de error
       fx = np.zeros_like(X)
       fy = np.zeros_like(Y)
       info_mensaje = f"Error en las ecuaciones: {str(error)}"

    # Construir la figura (se hace siempre, tanto en try como en except)
    fig = go.Figure()
    for i in range(n):
       for j in range(n):
          x0, y0 = X[i, j], Y[i, j]
          x1, y1 = x0 + fx[i, j], y0 + fy[i, j]

          fig.add_trace(go.Scatter(
              x=[x0, x1],
              y=[y0, y1],
              mode='lines+markers',
              line=dict(color='blue', width=2),
              marker=dict(size=[3, 5], color=['blue', 'red']),
              showlegend=False,
              hovertemplate=f"Punto: ({x0:.1f}, {y0:.1f})<br>Vector: ({fx[i, j]:.2f}, {fy[i, j]:.2f})"
          ))

    fig.update_layout(
        title=dict(
            text=f"<b>Campo Vectorial: dx/dt = {fx_str}, dy/dt = {fy_str}</b>",
            x=0.5, font=dict(size=16, color='black')
        ),
        xaxis_title="x",
        yaxis_title="y",
        paper_bgcolor='lightyellow',
        plot_bgcolor='white',
        font=dict(family='Outfit', size=12, color='black'),
        legend=dict(
            orientation="h", yanchor="bottom", y=0.88,
            xanchor="center", x=0.5
        ),
        margin=dict(l=20, r=40, t=80, b=40),
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        zeroline=True, zerolinewidth=2, zerolinecolor='gray',
        range=[-xmax*1.1, xmax*1.1]
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        zeroline=True, zerolinewidth=2, zerolinecolor='gray',
        range=[-ymax*1.1, ymax*1.1]
    )

    return fig, info_mensaje