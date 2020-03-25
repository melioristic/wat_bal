import matplotlib.pylab as plt
import numpy as np
from utils import read_parameters


class ParameterPlot(object):
    def __init__(self, parameters, names=["s_max", "rg", "k", "fr"]):
        self.num_param = len(names)
        self.parameters = parameters
        self.names = names
        
    def plot(self):
        fig = plt.figure()
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        for i in range(self.num_param):
            ax = fig.add_subplot(np.ceil(self.num_param/2), 2, i+1)
            ax.hist(self.parameters[:, i], bins=50)
            ax.set_xlabel(self.names[i])
        plt.savefig("plots/param_dist.png")


class OutputPlot(object):
    def __init__(self, q_obs, area, output):
        self.q_obs = q_obs
        self.output = output
        self.area = area
        self.var = ["q_sim", "et", "pot_et", "precipitation", "snow", "rainfall", "melt",
                    "snow_cover", "soil_storage", "q_surf" ,"groundwater_storage", "q_gw","temp", "temp_min", "temp_max"]
        self.x = np.arange(self.output.shape[0])
        self.right= self.x[-1]
        self.c0 = "#1f77b4"
        self.c1 = "#ff7f0e"
        self.c2 = "#2ca02c"
        self.c3 = "#d62728"
        self.linewidth = 0.5
    def plot_variables(self):

        self.et = self.output[:,1]
        self.pet = self.output[:,2]
        

        self.precipitation  = self.output[:,3]
        self.snow = self.output[:,4]
        self.rain = self.output[:,5]

        self.melt = self.output[:,6]

        self.snow_cover = self.output[:,7]

        self.snow_fraction = self.snow_cover/self.area

        self.temp_min = self.output[:,12]
        self.temp = self.output[:,13]
        self.temp_max = self.output[:,14]
        
        fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6))  = plt.subplots(3,2, figsize = (10,10))
   
        plt.subplots_adjust(wspace = 0.5, hspace = 0.75)

        ax1.plot(self.x, self.temp_min, linewidth = self.linewidth, label = "$T_{min}$")
        ax1.plot(self.x, self.temp, linewidth = self.linewidth, label = "$T_{av}$")
        ax1.plot(self.x, self.temp_max, linewidth = self.linewidth, label = "$T_{max}$")
        ax1.set_xlim(left = 0, right =self.right)
        ax1.set_ylabel("Temp [$\degree$C]")
        ax1.set_title("Daily $T_{min}$, $T_{av}$, and $T_{max}$")
        ax1.legend()

        ax2.plot(self.x, self.precipitation, linewidth = self.linewidth, label = "P")
        ax2.plot(self.x, self.rain, linewidth = self.linewidth, label = "R")
        ax2.plot(self.x, self.snow, linewidth = self.linewidth, label = "S")
        ax2.set_ylim(bottom =0)
        ax2.set_xlim(left = 0, right =self.right)
        ax2.set_ylabel("[mm/day]")
        ax2.set_title("Daily Precipitation Rain and Snow")
        ax2.legend()

        ax3.plot(self.x, self.pet, linewidth = self.linewidth, label = "PET")
        ax3.plot(self.x, self.et, linewidth = self.linewidth, label = "ET")
        ax3.set_xlim(left = 0, right =self.right)
        ax3.set_ylim(bottom =0)
        ax3.set_xlim(left = 0, right =self.right)
        ax3.set_ylabel("[mm/day]")
        ax3.set_title("Daily Actual and Potential Evapotranspiration")
        ax3.legend()

        ax4.plot(self.x, self.melt, linewidth = self.linewidth)
        ax4.set_xlim(left = 0, right =self.right)
        ax4.set_ylim(bottom =0)
        ax4.set_xlim(left = 0, right =self.right)
        ax4.set_ylabel("[mm/day]")
        ax4.set_title("Daily Snow Melt")
    
        ax5.plot(self.x, self.snow_cover, linewidth = self.linewidth)
        ax5.set_xlim(left = 0, right =self.right)
        ax5.set_ylim(bottom =0)
        ax5.set_xlim(left = 0, right =self.right)
        ax5.set_ylabel("[mm]")
        ax5.set_title("Snow Cover")
        
        ax6.plot(self.x, self.snow_fraction, linewidth = self.linewidth)
        ax6.set_xlim(left = 0, right =self.right)
        ax6.set_ylim(bottom =0)
        ax6.set_xlim(left = 0, right =self.right)
        ax6.set_ylabel("[mm]")
        ax6.set_title("Snow Cover Fraction")
        
        plt.savefig("plots/variables.png")


    def plot_runoff(self):
        self.soil_storage = self.output[:,8]
        self.surface_runoff = self.output[:,9]
        self.groundwater_storage = self.output[:,10]
        self.groundwater_runoff = self.output[:,11]

        fig, (ax1, ax3) = plt.subplots(2,1, figsize=(8,8))
        plt.subplots_adjust(hspace = 0.5)

        ax2 = ax1.twinx()
        ax4 = ax3.twinx()

        ax1.plot(self.x, self.soil_storage, linewidth = self.linewidth, label = "$S_{soil}$", color = self.c0)
        ax1.set_ylabel("$S_{soil}$ [mm]")
        ax1.set_ylim(bottom = 0, top = 40)
        ax1.set_xlim(left = 0, right = self.right)
        ax1.legend(loc = "upper left")

        ax2.plot(self.x, self.surface_runoff, linewidth = self.linewidth, label = "$Q_{surf}$", color = self.c1)
        ax2.set_ylabel("$Q_{surf}$ [mm]")
        ax2.set_ylim(bottom = 0, top = 10)
        ax2.set_xlim(left = 0, right = self.right)
        ax2.legend(loc = "upper right")
        ax2.set_title("Soil Storage and Surface Runoff")

        ax3.plot(self.x,self.groundwater_storage, linewidth = self.linewidth, label = "$S_{groundwater}$", color = self.c0)
        ax3.set_ylabel("$S_{groundwater}$ [mm]")
        ax3.set_ylim(bottom = 0, top = 220)
        ax3.set_xlim(left = 0,right = self.right)
        ax3.legend(loc = "upper left")

        ax4.plot(self.x,self.groundwater_runoff, linewidth = self.linewidth, label = "$Q_{groundwater}$", color = self.c1)
        ax4.set_ylabel("$Q_{groundwater}$ [mm]")
        ax4.set_ylim(bottom = 0, top = 20)
        ax4.set_xlim(left = 0, right = self.right)
        ax4.legend(loc = "upper right")
        ax4.set_title("Groundwater Storage and Groundwater Runoff")

        plt.savefig("plots/runoff.png")


    def plot_q(self):
        self.q_sim = self.output[:,0]
        fig, ax = plt.subplots(1,1 , figsize = (8,4))
        ax.plot(self.x,self.q_sim, color = self.c0, linewidth = self.linewidth, label = "$Q_{sim}$")
        ax.plot(self.x, self.q_obs, color = self.c1, linewidth = self.linewidth, label = "$Q_{obs}$")
        ax.set_ylabel("Q [mm/day]")
        ax.set_xlabel("Day (Julian)")
        ax.set_xlim(left = 0 , right = self.right)
        ax.set_ylim(bottom = 0)
        ax.set_title("Observed and Simulated Runoff")
        ax.legend()
        plt.savefig("plots/q.png")

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
        fig, ax = plt.subplots(figsize = (6,4))
        ax.plot(perc_sim,y, label = "Simulated Runoff")
        ax.plot(perc_obs,y, label = "Observed Runoff")
        ax.legend()
        ax.set_ylim(bottom = 0, top = 1)
        ax.set_xlim(left = 0)
        ax.set_xlabel("Discharge [mm/day]")
        ax.set_ylabel("F Cumulative")
        ax.set_title("Cumulative frequency distribution")
        plt.savefig("plots/percentile.png")

    def plot_scatter(self):
        self.q_sim = self.output[:,0]
        fig, ax = plt.subplots(1,1, figsize = (6,6))
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
        plt.savefig("plots/scatter.png")