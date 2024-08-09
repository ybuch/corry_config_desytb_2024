import argparse
import glob
import re
import os
import pandas as pd

data_folder = '/home/bgnet2/s3_cloud/beam_data/desy'
corry_bin = '~/corryvreckan/bin/corry'
geo_path_tel = '../geo/full_aligned'
geo_path_run = '../geo/temp'
dut_align_conf = '../conf/align_dut_mpx2.conf'
analysis_conf = '../conf/analysis.conf'
run_align_folder = '../geo/run_align'
analysis_folder = '../analysis'
run_start = 1400
run_stop = 1401
do_masking_per_run = True
do_analysis = True
number_of_events_align = 10000
number_of_events_analyze = 10000


df = pd.read_csv("../run_properties.csv", sep=",")
print(df)
data_in_files = glob.glob(data_folder + '/*.raw')
# print('available raws: ', data_in_files)



for current_run in range(run_start,run_stop+1):
    current_dut_file = ''
    current_tel_file = ''
    for f in data_in_files:
        m = re.search(f'mpx2.+run(0*{current_run})', f)
        if m:
            current_dut_file = f

        m = re.search(f'telescope.+run(0*{current_run})', f)
        if m:
            current_tel_file = f
    
    print(f'processing tel: {current_tel_file}, dut: {current_dut_file}')
    geo_id = df.loc[df['run_number'] == current_run]['geoid'].values[0]
    print(type(geo_id))
    tel_full_aligned = geo_path_tel+'/'+f'geo_id{geo_id}_full_aligned.geo'
    run_aligned = run_align_folder+'/'+f'alignment_run_{current_run}.geo'
    run_aligned_histo = '/'+f'alignment_run_{current_run}.root'
    analysis_histo = analysis_folder+'/'+f'analysis_run_{current_run}.root'

    if do_masking_per_run:
        print(f'Running alignment for run {current_run}')
        corry_cmd = f'{corry_bin} -c {dut_align_conf} -o number_of_events={number_of_events_align} -o output_directory={run_align_folder} -o detectors_file={tel_full_aligned} -o detectors_file_updated={run_aligned} -o histogram_file={run_aligned_histo} -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
        print(corry_cmd)
        os.system(corry_cmd)

        #Add mask file path to run aligned file
        with open(run_align_folder+'/'+f'alignment_run_{current_run}.geo', "r") as f:
            contents = f.readlines()

        index = contents.index('[Monopix2_0]\n')
        contents.insert(index+1, f'mask_file="../mask_files/applied_masks/mask_run{current_run}.txt"\n')

        with open(run_aligned, "w") as f:
            contents = "".join(contents)
            f.write(contents)

    if do_analysis:
        print(f'Running anaylsis for run {current_run}')
        corry_cmd = f'{corry_bin} -c {analysis_conf} -o number_of_events={number_of_events_analyze} -o output_directory={analysis_folder} -o detectors_file={run_aligned} -o histogram_file={analysis_histo} -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
        os.system(corry_cmd)
