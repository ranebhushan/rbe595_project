import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import numpy as np

import matplotlib
matplotlib.use('TKAgg')

path = '../Experiment_data/exp1/'

shared_req_data = {}
no_shared_req_data = {}
for filename in os.listdir(path):
    if filename.endswith(".csv"):
        # extract the parameters from the filename
        params = filename.split('_')
        num_robots = int(params[1])
        num_skills = int(params[2])
        num_tasks = int(params[3])
        sharing_flag = not('NO' in filename)
        
        # no_shared_req_data[num_robots] = {'min':0.0,'max':0.0,'mean':0.0,'std':0.0}
        if sharing_flag:
            sharing_df = pd.read_csv(path+filename)  
            # shared_req_data[num_robots] = {'min':10.0,'max':10.0,'mean':10.0,'std':10.0}
            # # print(num_robots, sharing_df['solving_time'].min(),sharing_df['solving_time'].max(),sharing_df['solving_time'].mean(),sharing_df['solving_time'].std()) 
            # shared_req_data[num_robots]['min'] = sharing_df['solving_time'].min()
            # shared_req_data[num_robots]['max'] = sharing_df['solving_time'].max()
            # shared_req_data[num_robots]['mean'] = sharing_df['solving_time'].mean()
            # shared_req_data[num_robots]['std'] = sharing_df['solving_time'].std()
            if not sharing_df.empty and not no_sharing_df.empty:
                plt.figure()
                sharing_df['best_path_length'].plot(label='Sharing')  
                no_sharing_df['best_path_length'].plot(label='NO Sharing')
                plt.title(str(num_robots) + " Robots "+str(num_skills) + " Skills "+str(num_tasks) + " Tasks ")
                plt.xlabel("No. of experiments")
                plt.ylabel("Best Path Length")
                plt.legend()
                temp = filename.split('.')[0]
                plt.savefig(f'{filename}.png',bbox_inches="tight",dpi=300)

        else:
            no_sharing_df = pd.read_csv(path+filename)
        #     #print(num_robots, sharing_flag, no_sharing_df['solving_time'].std()) 
        #     no_shared_req_data[num_robots]['min'] = no_sharing_df['solving_time'].min()
        #     no_shared_req_data[num_robots]['max'] = no_sharing_df['solving_time'].max()
        #     no_shared_req_data[num_robots]['mean'] = no_sharing_df['solving_time'].mean()
        #     no_shared_req_data[num_robots]['std'] = no_sharing_df['solving_time'].std()
            

# print(shared_req_data)
# x_data = list(shared_req_data.keys())
# x_data.sort()
# sorted = {str(i): shared_req_data[i] for i in x_data}
# print(sorted)
# labels = ['2R 1S 4T','4R 2S 8T','8R 4S 16T','16R 9S 32T','32R 19S 64T','64R 38S 128T']
# open_data=[]
# close_data=[]
# high_data=[]
# low_data=[]
# for every_key in sorted:
#     high_data.append(sorted[every_key]['max'])
#     low_data.append(sorted[every_key]['min'])
#     open_data.append(sorted[every_key]['mean']+sorted[every_key]['std']) 
#     close_data.append(sorted[every_key]['mean']-sorted[every_key]['std'])

    
# fig = go.Figure(data=[go.Candlestick(x=labels,open=open_data,high=high_data,low=low_data,close=close_data)])
# fig.update_layout(title="Time taken to solve the system",xaxis_title="Configuration",yaxis_title="Solving Time")
# fig.show()
    

    


        

        