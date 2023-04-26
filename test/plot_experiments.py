import pandas as pd
import matplotlib.pyplot as plt
import os

path = '../Experiment_data/'

dfs = []

for filename in os.listdir(path):
    if filename.endswith(".csv"):
        # extract the parameters from the filename
        params = filename.split('_')
        num_robots = int(params[1])
        num_skills = int(params[2])
        num_tasks = int(params[3])
        sharing_flag = not('NO' in filename)

        

        