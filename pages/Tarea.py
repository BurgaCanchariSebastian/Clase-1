import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go

dash.register_page(__name__, path="/pagina2", name="Página 2")


# --------- CARDS ----------
params_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Parámetros de Modelo", className="mb-0")),
        dbc.CardBody([
            # P0
            dbc.Label(["Población inicial (P0): ", html.Span(id="val-p0", className="fw-semibold ms-1")]),
            dcc.Slider(id="slider-p0", min=0, max=5000, step=10, value=820,
                       marks={0:"0", 1000:"1k", 3000:"3k", 5000:"5k"}, updatemode="drag"),

            dbc.FormText("Arrastra para ajustar P(0).", className="mb-3 d-block"),

            # r
            dbc.Label(["Tasa de crecimiento (r): ", html.Span(id="val-r", className="fw-semibold ms-1")]),
            dcc.Slider(id="slider-r", min=0.00, max=1.00, step=0.01, value=0.12,
                       marks={0.0:"0.00", 0.25:"0.25", 0.5:"0.50", 0.75:"0.75", 1.0:"1.00"},
                       updatemode="drag"),
            dbc.FormText("Arrastra para ajustar r.", className="mb-3 d-block"),

            # K
            dbc.Label(["Capacidad de carga (K): ", html.Span(id="val-k", className="fw-semibold ms-1")]),
            dcc.Slider(id="slider-k", min=100, max=10000, step=50, value=3000,
                       marks={100:"100", 2500:"2.5k", 5000:"5k", 7500:"7.5k", 10000:"10k"},
                       updatemode="drag"),
            dbc.FormText("Arrastra para ajustar k", className="mb-3 d-block"),

            # t
            dbc.Label(["Tiempo (t): ", html.Span(id="val-t", className="fw-semibold ms-1")]),
            dcc.Slider(id="slider-t", min=1, max=100, step=1, value=42,
                       marks={1:"1", 20:"20", 40:"40", 60:"60", 80:"80", 100:"100"},
                       updatemode="drag"),
            dbc.FormText("Arrastra para ajustar t.", className="mb-3 d-block"),

            dbc.Button("Generar gráfica", id="btn-generar", color="primary", className="mt-2"),
        ])
    ],
    className="shadow-lg rounded-4 bg-white text-dark h-100"  
)

graph_card = dbc.Card(
    [
        dbc.CardHeader(html.H5("Gráfica del Modelo", className="mb-0"), className="text-center"),
        dbc.CardBody([
            dcc.Graph(
                id="graph",
                style={"height": "520px"},        
                config={"displayModeBar": True},
                responsive=True
            )
        ])
    ],
    className="shadow-lg rounded-4 bg-white text-dark h-100",
)

# --------- LAYOUT ----------
layout = dbc.Container([
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(params_card, xs=12, lg=6, className="mb-4"),
                dbc.Col(graph_card,  xs=12, lg=6, className="mb-4"),
            ], className="g-4 align-items-stretch")
        ])
    ],
    className="shadow-lg rounded-4",
    style={"--bs-card-bg": "#AFE8FF"})
], fluid=True)





# --------- CALLBACKS ----------
@callback(
    Output("val-p0", "children"), Output("val-r", "children"),
    Output("val-k", "children"), Output("val-t", "children"),
    Input("slider-p0", "value"), Input("slider-r", "value"),
    Input("slider-k", "value"), Input("slider-t", "value"),
)
def show_values(p0, r, k, t):
    return f"{p0}", f"{r:.2f}", f"{k}", f"{t}"

@callback(
    Output("graph", "figure"),
    Input("btn-generar", "n_clicks"),
    Input("slider-p0", "value"), Input("slider-r", "value"),
    Input("slider-k", "value"), Input("slider-t", "value"),
    prevent_initial_call=False
)
def plot_logistic(_, p0, r, k, t):
    k = max(k, 1e-6); p0 = max(p0, 1e-6); t = max(t, 1)
    x = np.linspace(0, t, 400)
    y = k / (1 + ((k - p0)/p0) * np.exp(-r * x))
    fig = go.Figure()
    fig.add_scatter(x=x, y=y, mode="lines", name="P(t)")
    fig.update_layout(
        title={'text': 'Modelo logístico de crecimiento poblacional', 'x': 0.07},  
        xaxis_title="Tiempo(t)", yaxis_title="Población P(t)",
        height=520, margin=dict(l=50, r=30, t=50, b=50)
    )
    return fig
