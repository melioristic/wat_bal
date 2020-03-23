import matplotlib.pylab as plt
import numpy as np



class ParameterPlot(object):
    def __init__(self, parameters, names=["s_max", "rg", "k", "fr"]):
        num_param = len(names)
        fig = plt.figure()
        fig.subplots_adjust(hspace = 0.4, wspace = 0.4)
        for i in range(num_param):
            ax = fig.add_subplot(np.ceil(num_param/2),2,i+1)
            ax.hist(parameters[:,i])
            ax.set_xlabel(names[i])
        plt.show()


from utils import read_parameters

data = ParameterPlot(read_parameters())
