#!/usr/bin/env python
# coding: utf-8

#This script takes log files produced by corry jobsub as input and returns a csv with their efficiencies.
#The runnumbers are obtained from "run_properties.csv"


import numpy as np
import re
import pandas as pd
import glob
import csv


# Use glob to find all files matching the pattern '/*.log'

logs = glob.glob('<path_to_logfiles>/*.log')  #script written for logfiles from jobsub
run_map_file = '../run_properties.csv'
output_file = 'efficiencies.csv'

# Initialize a dictionary 'effis' to store efficiency-related data
effis = {'run_number': [], 'Efficiency': [], 'Err+': [], 'Err-':[]}

# append runnumbers from run_map_file
list1 = []
with open(run_map_file, mode ='r')as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
      list1.append(lines[0])
list1.pop(0)

# conversion of the runnumbers to np.array
list1=list(map(int, list1))
runs_to_analyse = np.array(list1)

logs.sort()
filesToRemove = []

# delete runnumbers in list which are not in run_map_file
for r in logs:
    match = re.search(r'analysis_jobsub_(\d+)', r)
    if match:
        runNmb = int(match.group(1))
        if not (runNmb in runs_to_analyse):
            filesToRemove.append(r)
    else:
        filesToRemove.append(r)

for f in filesToRemove:
    logs.remove(f)

logs.sort()

# Loop through each file found by glob
for f in logs:
    with open(f) as log:  # Open the file for reading
        for line in log:  # Loop through each line in the file

            # Use regular expressions to search for a pattern in the line
            # Explanation of the regex pattern:
            # (?<=Total efficiency ) - Positive lookbehind for "Total efficiency "
            # .+ - Match one or more of any character (except newline)
            # (\d\d\.\d+) - Capture a numerical value in the format of two digits, a dot, and one or more digits (Efficiency)
            # \(.(0.\d+) .(0.\d+)' - Capture two numerical values in parentheses (Err+ and Err-)
            match = re.search(r'(?<=Total efficiency )(.+(\d\d\.\d+)\(.(0.\d+) .(0.\d+))', line)
            #print(match)
            
            if not match:
                continue  # If no match is found, skip to the next line

            runNmb = int(re.search(r'analysis_jobsub_(\d+)', f).group(1))
            # Extract and store data based on the regular expression groups
            effis['run_number'].append(runNmb)  # Extract 'Bias' from the file name
            effis['Efficiency'].append(float(match.group(2)))  # Extract 'Efficiency' value
            effis['Err+'].append(float(match.group(3)))  # Extract 'Err+' value
            effis['Err-'].append(float(match.group(4)))  # Extract 'Err-' value

df = pd.DataFrame(effis)
df.to_csv(output_file, index=False)




