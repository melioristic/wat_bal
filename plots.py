import matplotlib.pylab as plt
import numpy as np
from utils import read_parameters


class ParameterPlot(object):
    def __init__(self, parameters, names=["s_max", "rg", "k", "fr"]):
        num_param = len(names)
        fig = plt.figure()
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        for i in range(num_param):
            ax = fig.add_subplot(np.ceil(num_param/2), 2, i+1)
            ax.hist(parameters[:, i], bins=50)
            ax.set_xlabel(names[i])
        plt.show()


class OutputPlot(object):
    def __init__(self, q_obs, output):
        self.q_obs = q_obs
        self.output = output
        self.var = ["q_sim", "et", "pot_et", "precipitation", "snow", "rainfall", "melt",
                    "snow_cover", "soil_storage", "groundwater_storage", "temp", "temp_min", "temp_max"]
        self.x = np.arange(self.output.shape[0])

    def plot_et(self):
        self.et = self.output[:, 1]
        self.pet = self.output[:, 2]
        plt.plot(self.x, self.et)
        plt.plot(self.x, self.pet)
        plt.show()

    def plot_temp(self):
        self.temp_min = self.output[:, 8]
        self.temp = self.output[:, 9]
        self.temp_max = self.output[:, 10]
        plt.plot(self.x, self.temp_min)
        plt.plot(self.x, self.temp)
        plt.plot(self.x, self.temp_max)
        plt.show()

    def plot_precipitation(self):
        self.precip = self.output[:, 3]
        self.snow = self.output[:, 4]
        self.rainfall = self.output[:, 5]
        plt.plot(self.x, self.precip)
        plt.plot(self.x, self.snow)
        plt.plot(self.x, self.rainfall)
        plt.show()

    def plot_melt(self):
        self.melt = self.output[:,5]
        plt.plot(self.x,self.melt)
        plt.show()
    
    def plot_q(self):
        self.q_sim = self.output[:,0]
        fig, ax = plt.subplots()
        ax.plot(self.x,self.q_sim, color = "seagreen")
        ax.plot(self.x, self.q_obs, color = "rebeccapurple")
        ax.legend(["$Q_{sim}$", "$Q_{obs}$"])
        
        ax.set_ylabel("Q [mm/day]")
        ax.set_xlabel("Day (Julian)")
        plt.show()

    def plot_percentile(self):
        self.q_sim = self.output[:,0]
       
        num_points = 101
        y = np.zeros(num_points)
        perc_sim = np.zeros(num_points)
        perc_obs = np.zeros(num_points)

        for i in range(num_points):
            perc_sim[i] = np.percentile(self.q_sim,i*101/num_points)
            perc_obs[i] = np.percentile(self.q_obs,i*101/num_points) 
            y[i] = i*101/num_points/100
        fig, ax = plt.subplots()
        ax.plot(perc_sim,y, color = "seagreen")
        ax.plot(perc_obs,y, color = "rebeccapurple")
        ax.legend(["Simulation", "Observation"])
        ax.set_ylim(bottom = 0, top = 1)
        ax.set_xlim(left = 0)
        ax.set_xlabel("Discharge [mm/day]")
        ax.set_ylabel("F Cumulative")
        ax,set_title("Observed and Simulated Daily Runoff")
        plt.show()

    def plot_scatter(self):
        self.q_sim = self.output[:,0]
        fig, ax = plt.subplots()
        x_values = [1e-3, 1e4]
        y_values = [1e-3, 1e4]
        ax.plot(x_values, y_values, color = "k", linestyle = "--", alpha = 0.5)
        ax.scatter(self.q_obs,self.q_sim, marker = "o",s=1, color = "b")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(left = 1e-3, right=1e4)
        ax.set_ylim(bottom = 1e-3, top=1e4)
        ax.set_xlabel("$Q_{obs}$ [mm/day]")
        ax.set_ylabel("$Q_{sim}$ [mm/day]")
        ax.set_title("Scatter plot of Simulated vs Observed Discharge")
        plt.show()