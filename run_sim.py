from model import VariablePrep, ConceptualWatbalModel
from utils import read_parameters, GOF
import numpy as np
from plots import OutputPlot

file_name = "LATTERBACHmeteo.txt"
var = VariablePrep(file_name, cal_factor=0, cal_data=False, val_data=True)

# Manually enter the parameter values after seeing the plot

param = {"s_max": 39.4039,
         "rg": 17.9764,
         "k": 0.8265,
         "fr": 0.0688
         }

num_time_steps = var.j_day.shape[0]

output = np.zeros((var.j_day.shape[0], 15))

for step in range(num_time_steps):
    variables = {
        "j_day": var.j_day[step],
        "temp": var.t_av[step],
        "temp_max": var.t_max_av[step],
        "temp_min": var.t_min_av[step],
        "precip": var.precip[step]
    }
    if step == 0:
        model = ConceptualWatbalModel(parameters=param)
        output[step] = model.simulate(variables=variables)
    else:
        output[step] = model.simulate(variables=variables)


gof_class = GOF(sim=output[:, 0], obs=var.q)
gof_class.save_gof()


plot_class = OutputPlot(var.q, var.area, output)
plot_class.plot_variables()
plot_class.plot_runoff()
plot_class.plot_q()
plot_class.plot_percentile()
plot_class.plot_scatter()
