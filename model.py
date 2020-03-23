import numpy as np
import matplotlib.pylab as plt
import math
from utils import read_data

class VariablePrep(object):
    def __init__(self, filename = "LATTERBACHmeteo.txt", cal_factor = 0.8, cal_data = True, val_data = False):
        
        self.area = 562 # in km2
        self.elevation_basin = 1590 # mean elevation of the catchment
        self.elevation_station = 1320 # elevation of the measuring station
        self.lapse_rate = 0.5/100 # lapse rate for temperature in Celsius/metre

        assert val_data != cal_data , "Select one of cal_data or val_data"
        j_day, precip, t_max, t_min , q  = read_data(filename)
    
        div_index = np.floor(cal_factor*j_day.shape[0])
        
        if cal_data:
            self.j_day = j_day[:div_index]
            self.precip = precip[:div_index]
            self.t_max = t_max[:div_index]
            self.t_min = t_min[:div_index]
            self.q = q[:div_index]
        elif val_data:
            self.j_day = j_day[div_index:]
            self.precip = precip[div_index:]
            self.t_max = t_max[div_index:]
            self.t_min = t_min[div_index:]
            self.q = q[div_index:]

        self.q_obs = 1000*(self.q*60*60*24)/(self.area*10e6)

        self.t_min_av = (self.elevation_station-self.elevation_basin)*self.lapse_rate + self.t_min
        self.t_max_av = (self.elevation_station-self.elevation_basin)*self.lapse_rate + self.t_max

        self.t_av = (self.t_min_av+self.t_max_av)/2


class ConceptualWatbalModel(object):
    def __init__(self, parameters):
        self.flow_prev = 0
        self.snow_cover_prev = 0
        self.ss_prev = 0
        self.sg_prev = 0

        self.k = parameters["k"]
        self.s_max = parameters["s_max"]
        self.fr = parameters["fr"]
        self.rg = parameters["rg"]

    def divide_snow_rain(self):
        if self.temp_max <= 0:
            self.snow = self.precipitation
            self.rainfall = 0
        
        if self.temp_min > 0:
            self.snow = 0
            self.rainfall = self.precipitation 

        if (self.temp_max > 0 and self.temp_min<=0):
            self.rainfall = self.temp_max/(self.temp_max-self.temp_min)*self.precipitation
            self.snow = self.precipitation - self.rainfall
    
    def compute_snow_melt(self, temp_snow_melt = 0):
        self.temp_snow_melt = temp_snow_melt
        
        if self.temp <= self.temp_snow_melt:
            self.melt = 0
        elif self.temp > self.temp_snow_melt:
            self.melt = min(self.k*(self.temp-self.temp_snow_melt),self.snow_cover_prev)

    def compute_snow_cover(self):
        self.snow_cover_current= self.snow_cover_prev - self.melt + self.snow
        
    
    def compute_pot_et(self, lat = 46.5):
        phi = lat
        delta  = 0.4093*np.sin((2*math.pi/365)*self.j_day-1.405)
        omega_s = np.arccos(-np.tan(2*np.pi*phi/360)*np.tan(delta))
        Nt = 24*omega_s/np.pi
        a, b, c = 0.6108, 17.27, 237.3
        es = a*np.exp(b*self.temp/(self.temp+c))
        E = (2.1*(Nt**2)*es/(self.temp+273.3))
        
        if self.temp <= 0:
            E = 0
        self.pot_et =  E   

    def compute_et(self):
        
        self.et = self.ss_prev/self.s_max*self.pot_et

    def compute_soil_zone_water_content(self):
        self.ss_current = self.ss_prev +self.melt+self.rainfall-self.et
        if self.ss_current < 0 :
            self.ss_current = 0
    
    def compute_surface_runoff(self):
        
        if self.ss_current > self.s_max:
            self.q_surf = (self.rainfall+self.melt)*self.fr
            self.ss_current = self.ss_current - self.q_surf
        else:
            self.q_surf = 0

    def compute_percolation_groundwater(self):
        if self.ss_current >self.s_max:
            self.perc_gw = self.ss_current - self.s_max
            self.ss_current = self.ss_current-self.perc_gw

        else:
            self.perc_gw = 0

    def compute_ground_water_reservoir(self):
        self.q_gw = 1/self.rg*self.sg_prev
        self.sg_current = self.sg_prev + self.perc_gw - self.q_gw
        if self.ss_current<0:
            self.q_gw = 0
            self.sg_current = 0

    def compute_stream_flow(self):
        self.q_out = self.q_surf + self.q_gw

    def update(self):
        self.snow_cover_prev = self.snow_cover_current
        self.ss_prev = self.ss_current
        self.sg_prev = self.sg_current

    def simulate(self, variables):
        
        self.j_day = variables["j_day"]
        self.temp_max = variables["temp_max"]
        self.temp_min = variables["temp_min"]
        self.temp = variables["temp"]
        self.precipitation = variables["precipitation"]

        self.divide_snow_rain()
        self.compute_snow_melt()
        self.compute_snow_cover()
        self.compute_pot_et()
        self.compute_et()
        self.compute_soil_zone_water_content()
        self.compute_surface_runoff()
        self.compute_percolation_groundwater()
        self.compute_ground_water_reservoir()
        self.compute_stream_flow()
        self.update()
        return self.q_out

    def get_temp(self):
        return self.temp_min, self.temp, self.temp_max
    
    def get_precip(self):
        return self.precipitation, self.rainfall, self.snow
    
    def get_evapotranspiration(self):
        return self.et, self.pot_et

    def get_melt(self):
        return self.melt
    
    def get_snow_cover(self):
        return self.snow_cover_current

    