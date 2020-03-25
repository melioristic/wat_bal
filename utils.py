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
    with h5py.File("parameters.h5","r") as f:
        nruns = len(f.keys())-1
        param_arr = np.zeros((nruns,4))
        for run in range(nruns):
            param_arr[run,:] = f.get("params_"+str(run))[:]

    return param_arr

class GOF(object):
    def __init__(self, sim, obs):
        self.sim = sim
        self.obs = obs

    def mean_error(self):
        return np.mean(self.obs-self.sim)
    
    def percent_bias(self):
        return 100*(np.mean(self.sim)-np.mean(self.obs))/np.mean(self.obs)
    
    def mean_absolute_error(self):
        return np.mean(np.abs(self.obs-self.sim))

    def root_mean_square_error(self):
        return np.sqrt(np.mean(np.square(self.obs-self.sim)))
    
    def nash_shutcliffe_efficiency(self):
        numerator = np.sum(np.square(self.obs-self.sim))
        denominator = np.sum(np.square(self.obs-np.mean(self.obs)))
        return 1-numerator/denominator

    def index_of_agreement(self):
        numerator = np.sum(np.square(self.obs-self.sim))
        denominator = np.sum(np.square((np.abs(self.sim-np.mean(self.sim)))+(np.abs(self.obs-np.mean(self.obs)))))

        return 1-numerator/denominator

    def save_gof(self):
        me = self.mean_error()
        pb = self.percent_bias()
        mae = self.mean_absolute_error()
        rmse = self.root_mean_square_error()
        nse = self.nash_shutcliffe_efficiency()
        ioa = self.index_of_agreement()

        data = np.array([me, pb, mae, rmse, nse, ioa]).reshape(1,6)
      
        col_names = ["Mean Error", "Percent Bias","Mean Absolute Error", "Root Mean Square Error", "Nash-Shutcliffe-Efficiency", "Index of Agreement"]

        for i in range(len(col_names)):
            print(f"{col_names[i]}  : {np.round(data[0,i],3)}")
 
        gof = pd.DataFrame(data = data, columns = col_names)
        gof.to_csv("gof.csv")