import pandas as pd
import numpy as np


class Model:
    k1 = 0.0468
    k2 = 2510
    k3 = 3.14 * 10 ** (-6)
    k4 = 1.92 * 10 ** (-6)
    t_step = 0.001
    h2o = 15500
    n2 = 780000
    df = pd.DataFrame()

    def __init__(self):
        pass

    def fit(self, x0, t_spam):
        self.t_step = t_spam[2]
        t = np.arange(t_spam[0], t_spam[1], self.t_step)
        o3, no2, no3, n2o5, hno3 = [x0[0]], [x0[1]], [x0[2]], [x0[3]], [x0[4]]

        for i in range(len(t) - 1):
            r1 = self.t_step * self.k1 * o3[i] * no2[i]
            r2 = self.t_step * self.k2 * no2[i] * no3[i]
            r3 = self.t_step * self.k3 * n2o5[i] * self.n2
            r4 = self.t_step * self.k4 * n2o5[i] * self.h2o

            o3.append(o3[i] - r1)
            no2.append(no2[i] - r1 - r2 + r3)
            no3.append(no3[i] + r1 - r2 + r3)
            n2o5.append(n2o5[i] + r2 - r3 - r4)
            hno3.append(hno3[i] + 2 * r4)

        aux = ['O3', 'NO2', 'NO3', 'N2O5', 'HNO3']
        names = []
        times = []
        for nam in aux:
            names.extend([nam for _ in range(len(t))])
            times.extend(t)

        self.df = pd.DataFrame({
            'time (min)': times,
            'concentrations (ppm)': o3 + no2 + no3 + n2o5 + hno3,
            'molecule': names
        })

        return None

    def predict(self):
        return self.df
