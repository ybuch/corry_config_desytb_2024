#!/usr/bin/env python
# coding: utf-8

# This script reads rootfiles given in 'run_properties.csv' and extracts the keys ToT, Cluster size and Spatial Resolution to seperate csv files


import uproot
import pandas as pd
import glob
import numpy as np
import hist
import re
import csv


# Define a list of ROOT files to open

root_file_list = glob.glob('<path_to_rootfiles>/*.root')
run_map_file = '../run_properties.csv'
output = ["root_data_ToT.csv",'root_data_cluster.csv','root_data_residual.csv']


# Define a list of keys (TKeys) to extract data from
#efficiency not working properly

keys_to_extract = [["EventLoaderEUDAQ2/Monopix2_0/hPixelRawValues", "ToT (LSB)"],
        ["ClusteringSpatial/Monopix2_0/clusterSize", "Cluster size"],
        ["AnalysisDUT/Monopix2_0/local_residuals/residualsX", r"Spatial Resolution X ($\mu m$)"]]


# extract runnumbers from run_map_file
run_map = {}
list1 = []
with open(run_map_file, mode ='r')as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
      list1.append(lines[0])
list1.pop(0)
list1=list(map(int, list1))
runs_to_analyse = np.array(list1)

# find matching root files for each runnumber
root_file_list.sort()
filesToRemove = []
for r in root_file_list:
    match = re.search(r'(\d+)\.root', r)
    if match:
        runNmb = int(match.group(1))
        if not (runNmb in runs_to_analyse):
            filesToRemove.append(r)
    else:
        filesToRemove.append(r)

for f in filesToRemove:
    root_file_list.remove(f)
    
root_file_list.sort()


# read csv, create run_map
with open(run_map_file) as f:
    for line in f:
        if line.startswith('r'): # ugly way to skip header
            continue
        run, chip_id, frontend, threshold, bias, temp, run_type, elog_curve, elog_run = line.split(',')
        run = int(run)
        temp = abs(float(temp))
        run_map[run] = run


# Create an empty DataFrame to store the results
# results_df = pd.DataFrame(columns=["File", "Key", "Mean", "StdDev"])
results = {"File" : [],"run_number": [], "Key" : [], "Name" : [], "Mean" : [], "StdDev": [], "StdErr" : []}

# Loop over each ROOT file
for root_file in root_file_list:
    # Open the ROOT file using uproot
    with uproot.open(root_file) as file:
        # Loop over each key to extract data
        for key_name in keys_to_extract:
            try:
                # Access the TKey using the key name
                tkey = file[key_name[0]]
                #print(tkey)
                mean_val = 0
                std_dev_val = 0
                N = 0
                # Check if the TKey points to a TH1F histogram
                if isinstance(tkey, uproot.uproot.behaviors.TH1.TH1):                    
                    hist_np = tkey.to_numpy() # [0] ... bins, [1] ... weights
                    # hist_data = tkey.to_hist()
                    # hist_data.plot()
                    # plt.show()
                        
                    unjagged_bins = (hist_np[1][:-1] + hist_np[1][1:]) / 2
                    
                    N = np.sum(hist_np[0])
                    mean_val = np.sum(hist_np[0] * unjagged_bins) / N
                    #print('mean = ', mean_val)                    
                    std_dev_val = np.sqrt(np.sum(hist_np[0] * (unjagged_bins - mean_val)**2) / N)

                    #hacky special treatment
                    if 'hPixelRawValues' in key_name[0]:
                        mask = unjagged_bins < 100
                        N = np.sum(hist_np[0][mask])
                        mean_val = np.sum(hist_np[0][mask] * unjagged_bins[mask]) / N
                        std_dev_val = np.sqrt(np.sum(hist_np[0][mask] * (unjagged_bins[mask] - mean_val)**2) / N)
                    #print('std', std_dev_val)
                elif isinstance(tkey, uproot.uproot.behaviors.TProfile2D.TProfile2D):
                    # print('encountered a', tkey)
                    vals = tkey.values()
                    # print(vals, np.average(vals))
                    mean_val = np.average(vals)
                    std_dev_val = np.std(vals)
                    N = 1
                else:
                    continue

                runNmb = int(re.search(r'(\d+)\.root', root_file).group(1))
                results["run_number"].append(run_map[runNmb])
                results["Mean"].append(mean_val)
                results['StdDev'].append(std_dev_val)
                results['File'].append(root_file)
                results['Key'].append(key_name[0])
                results['Name'].append(key_name[1])
                results["StdErr"].append(std_dev_val / np.sqrt(N))

            except KeyError:
                print(f"Key '{key_name}' not found in file '{root_file}'")

df = pd.DataFrame(results)

## create csv with all data
#df.to_csv('root_data_W08R06.csv', index=False,  columns=["run_number","Name","Mean","StdDev","StdErr"])

# write seperate csv file for each key
df_ToT = df[df['Name']=="ToT (LSB)"]
df_cluster = df[df['Name']=="Cluster size"]
df_residual = df[df['Name']=="Spatial Resolution X ($\mu m$)"]

df_ToT.to_csv(output[0], index=False,  columns=["run_number","Mean","StdDev","StdErr"])
df_cluster.to_csv(output[1], index=False,  columns=["run_number", "Mean","StdDev","StdErr"])
df_residual.to_csv(output[2], index=False,  columns=["run_number","Mean","StdDev","StdErr"])





