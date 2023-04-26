import matplotlib.pyplot as plt
import numpy as np
import sys
import os

class Plotter:
    def __init__(self):
        pass

    def plot(self, x, y, x_label, y_label, title, filename):
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.savefig(filename)
        plt.close()