import dash_bootstrap_components as dbc


def inputr(id_, text):
    f = dbc.Input(id=id_,
                  placeholder=text,
                  style={'margin-top': '25px'})
    return f
