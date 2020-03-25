from utils import read_parameters
from plots import ParameterPlot

parameters = read_parameters()
param_plot = ParameterPlot(parameters)
param_plot.plot()
