import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

import numpy as np
import plotly.express as px
import model as m
import controls as c

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])
server = app.server

control_panel = dbc.Card(
    dbc.CardBody([
        html.P(r'Initial Conditions (ppm)'),
        c.inputr('id_o3', '[O3]0'),
        c.inputr('id_no2', '[NO2]0'),
        c.inputr('id_no3', '[NO3]0'),
        c.inputr('id_n2o5', '[N2O5]0'),
        c.inputr('id_hno3', '[HNO3]0'),
        html.Hr(),
        html.P(r'Time (min)'),
        c.inputr('t0', 't0'),
        c.inputr('tf', 'tf'),
        c.inputr('step', 'time step'),
        dbc.Button(id='gerar', children='Generate', style={'margin-top': '20px'}),
    ]),
    style={'height': '100vh'}
)

app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col(control_panel, width=2),
        dbc.Col(dcc.Loading(dcc.Graph(id='graph', style={'height': '100vh'})), width=10)
    ], no_gutters=True)
])


@app.callback(
    Output('graph', 'figure'),
    Input('gerar', 'n_clicks'),
    State('id_o3', 'value'),
    State('id_no2', 'value'),
    State('id_no3', 'value'),
    State('id_n2o5', 'value'),
    State('id_hno3', 'value'),
    State('t0', 'value'),
    State('tf', 'value'),
    State('step', 'value')
)
def f_callback(c, x0, x1, x2, x3, x4, t0, tf, t_step):
    def is_float(x):
        try:
            float(x)
            return True
        except:
            return False

    t_spam = [t0, tf, t_step]
    initial_cond = [x0, x1, x2, x3, x4]

    if c is None:
        initial_cond = ['0.15', '0.20', '0.', '0.', '0.']
        t_spam = [0, 200, 0.0001]

    numeric = [not is_float(x) for x in initial_cond]
    numeric2 = [not is_float(x) for x in t_spam]
    if any(numeric) | any(numeric2):
        raise dash.exceptions.PreventUpdate

    initial_cond = [float(num) for num in initial_cond]
    t_spam = [float(num) for num in t_spam]

    model = m.Model()
    model.fit(initial_cond, t_spam)
    df = model.predict()
    index = np.arange(0, len(df), len(df) / 200)
    return px.line(df[df.index.isin(index)],
                   x='time (min)',
                   y='concentrations (ppm)',
                   color='molecule',
                   template='plotly_dark')


if __name__ == '__main__':
    app.run_server(debug=True)
