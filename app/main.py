import model as m
import numpy as np
import plotly.express as px

initial_cond = [0.15, 0.20, 0., 0., 0.]
t_spam = [0, 200, 0.0001]

if __name__ == '__main__':
    model = m.Model()
    model.fit(initial_cond, t_spam)
    df = model.predict()
    index = np.arange(0, len(df), len(df) / 200)

    fig = px.line(df[df.index.isin(index)], 'time (min)', 'concentrations (ppm)', color='molecule')
    fig.show()
