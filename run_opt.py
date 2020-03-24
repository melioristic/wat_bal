from model import VariablePrep , ConceptualWatbalModel
from utils import read_data
import numpy as np
import scipy.optimize
from scipy.optimize import Bounds
import h5py 
from tqdm import tqdm
import time 
import matplotlib.pyplot as plt


def optimize_model(parameters):
    # read data function is in the utils folder and reads
    #j_day = Julian Day
    #precip = precipitation in mm
    #t_max = maximum daily temperature
    #t_min = minimum daily temperature
    #q = daily discharge in m3/s

    file_name = "LATTERBACHmeteo.txt" 
    var = VariablePrep(file_name, cal_factor = 0.8, cal_data = True, val_data = False)

    ####### Simulation 
    # s_max = 40 # soil_zone_water_capacity
    # rg = 20 # groundwater linear reser
    # k = 1 # daily degree snowmelt parameter
    # fraction_imperv = 0.3 # Fraction of basin area that is importvious
    
    param = {"s_max":parameters[0], 
            "rg":parameters[1],
            "k":parameters[2],
            "fr": parameters[3]
            }

    #model  = ConceptualWatbalModel(param)

    num_time_steps = var.j_day.shape[0]

    output = np.zeros((var.j_day.shape[0],8))

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
            output[step,:] = model.simulate(variables = variables)
        else:
            output[step,:] = model.simulate(variables=variables)

    q_sim = output[:,0]
    q_obs = var.q
    return np.sqrt(np.mean((q_obs - q_sim)**2))

nruns =  1

## Create an empty h5 file.
## This line rewrites the parameters.h5 file.
## If parameters.h5 file is already there delete this file
with h5py.File("data/parameters.h5","w") as f:
        # Do nothing just create the folder
    f.create_dataset("runs", data = [nruns])

    for run in tqdm(range(nruns)):
        start_time = time.time()
        lb = [30,5,0.4,0]
        ub = [60,60,2,0.2]

        init_s_max = np.random.uniform(low  = lb[0], high=ub[0])
        init_rg = np.random.uniform(low = lb[1], high=ub[1])
        init_k = np.random.uniform(low = lb[2], high=ub[2])
        init_fr = np.random.uniform(low = lb[3], high=ub[3])

        initial_guess = [init_s_max, init_rg, init_k, init_fr]
        bounds = Bounds(lb=lb, ub=ub)
        result = scipy.optimize.minimize(fun=optimize_model, x0=initial_guess, method="L-BFGS-B", bounds = None)
        opt_param = result.x
        
        f.create_dataset("params_"+str(run), data=np.array(opt_param))
        #print(f"Completed {np.round((run+1)/nruns*100,2)} % in {time.time()-start_time} seconds")
