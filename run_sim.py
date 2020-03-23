from model import VariablePrep, ConceptualWatbalModel
from utils import read_parameters
import numpy as np

file_name = "LATTERBACHmeteo.txt" 
var = VariablePrep(file_name, cal_factor = 0.8, cal_data = False, val_data = True)

parameters = read_parameters()


param = {"s_max":parameters[0], 
            "rg":parameters[1],
            "k":parameters[2],
            "fr": parameters[3]
            }

num_time_steps = var.j_day.shape[0]

output = np.zeros((var.j_day.shape[0],1))

for step in range(num_time_steps):
    variables = {
        "j_day":var.j_day[step],
        "temp":var.t_av[step],
        "temp_max":var.t_max_av[step],
        "temp_min":var.t_min_av[step],
        "precipitation":var.precip[step]
    }
    if step == 0:
        model = ConceptualWatbalModel(parameters = param)
        output[step] = model.simulate(variables = variables)
    else:
        output[step] = model.simulate(variables=variables)