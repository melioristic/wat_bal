import pandas as pd
import h5py
import numpy as np


def read_data(filename = "HONDRICHmeteo.txt"):

    data = pd.read_csv("data/"+filename, delimiter="\t", skiprows=1)

    j_day = data.day.values
    precip = data.P_mix.values
    t_max = data.T_max.values    
    t_min = data.T_min.values    
    q = data.Q.values

    return j_day, precip, t_max, t_min, q

def read_parameters():
    with h5py.File("data/parameters.h5","r") as f:
        print(f.keys())
        nruns = len(f.keys())-1
        param_arr = np.zeros((nruns,4))
        for run in range(nruns):
            print(f.get("params_"+str(run))[:])
            param_arr[run,:] = f.get("params_"+str(run))[:]

    return param_arr
