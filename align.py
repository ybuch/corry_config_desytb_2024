import argparse
import glob
import re
import os

data_folder = '/home/akumar/vtx_belle2/analysis/beam/2024_07_DESY/data/beam_data/desy'
corry_bin = '/home/akumar/vtx_belle2/corryvreckan/bin/corry'
corry_config_create_mask_all = 'createmask.conf'
corry_config_prealign_all = 'prealign.conf'
corry_config_align_tel = 'align_tel_mpx2.conf'
corry_config_align_dut = 'align_dut_mpx2.conf'
geo_path = '/home/akumar/vtx_belle2/analysis/beam/2024_07_DESY/corry_config_desytb_2024/geometries/'
output_dir = '/home/akumar/vtx_belle2/analysis/beam/2024_07_DESY/corry_config_desytb_2024/align_out'

parser = argparse.ArgumentParser(description='corry alignment wrapper')
parser.add_argument('-r', help='run number', required=True)
#parser.add_argument('--start', help='run number start')
#parser.add_argument('--stop', help='run number stop')
parser.add_argument('-g', help='new geoid number', required=True)
parser.add_argument('-o', help='old geoid number. If specified telescope alignment with given geoid will be used and only DUT will be aligned.')
parser.add_argument('-n', help='number of events', default = 50000)


args = parser.parse_args()

data_in_files = glob.glob(data_folder + '/*.raw')
# print('available raws: ', data_in_files)

current_run = args.r
number_of_events = args.n


output_file = f'analysis_run{current_run}.root'

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
rough_geo = geo_path + f'geoid{args.g}.geo'
mask_geo = geo_path + f'geoid{args.g}_{args.r}_masked.geo'
prealign_geo = geo_path + f'geoid{args.g}_{args.r}_prealigned.geo'
align_tel_geo_itr1 = geo_path + f'geoid{args.g}_{args.r}_tel_aligned_itr1.geo'
align_tel_geo_itr2 = geo_path + f'geoid{args.g}_{args.r}_tel_aligned_itr2.geo'
align_tel_geo_itr3 = geo_path + f'geoid{args.g}_{args.r}_tel_aligned_itr3.geo'
align_tel_geo_itr4 = geo_path + f'geoid{args.g}_{args.r}_tel_aligned_itr4.geo'
align_tel_geo = geo_path + f'geoid{args.g}_{args.r}_tel_aligned.geo'
align_dut_geo_itr1 = geo_path + f'geoid{args.g}_{args.r}_dut_aligned_itr1.geo'
align_dut_geo_itr2 = geo_path + f'geoid{args.g}_{args.r}_dut_aligned_itr2.geo'
align_dut_geo_itr3 = geo_path + f'geoid{args.g}_{args.r}_dut_aligned_itr3.geo'
align_dut_geo = geo_path + f'geoid{args.g}_{args.r}_dut_aligned.geo'

if not args.o:

    print('\n\n###### create mask #########')
    corry_cmd = f'{corry_bin} -c {corry_config_create_mask_all} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={rough_geo} -o detectors_file_updated={mask_geo} -o histogram_file=geoid{args.g}_{args.r}_masking.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file} -g MIMOSA26_0.mask_file="../maskfiles/mask_ref0_run{args.r}.txt" -g MIMOSA26_1.mask_file="../maskfiles/mask_ref1_run{args.r}.txt" -g MIMOSA26_2.mask_file="../maskfiles/mask_ref2_run{args.r}.txt" -g MIMOSA26_3.mask_file="../maskfiles/mask_ref3_run{args.r}.txt" -g MIMOSA26_4.mask_file="../maskfiles/mask_ref4_run{args.r}.txt" -g MIMOSA26_5.mask_file="../maskfiles/mask_ref5_run{args.r}.txt" -g Monopix2_0.mask_file="../maskfiles/mask_dut_run{args.r}.txt"'
    os.system(corry_cmd)

    print('\n\n###### pre-alignment all #########')
    corry_cmd = f'{corry_bin} -c {corry_config_prealign_all} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={mask_geo} -o detectors_file_updated={prealign_geo} -o histogram_file=geoid{args.g}_{args.r}_prealigned_all.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)


    print('\n\n###### alignment telescope 1 #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_tel} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={prealign_geo} -o detectors_file_updated={align_tel_geo_itr1} -o histogram_file=geoid{args.g}_{args.r}_tel_aligned_itr1.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n\n###### alignment telescope 2 #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_tel} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_tel_geo_itr1} -o detectors_file_updated={align_tel_geo_itr2} -o histogram_file=geoid{args.g}_{args.r}_tel_aligned_itr2.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n\n###### alignment telescope 3 #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_tel} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_tel_geo_itr2} -o detectors_file_updated={align_tel_geo_itr3} -o histogram_file=geoid{args.g}_{args.r}_tel_aligned_itr3.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n\n###### alignment telescope 4 #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_tel} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_tel_geo_itr3} -o detectors_file_updated={align_tel_geo_itr4} -o histogram_file=geoid{args.g}_{args.r}_tel_aligned_itr4.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n\n###### alignment telescope final #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_tel} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_tel_geo_itr4} -o detectors_file_updated={align_tel_geo} -o histogram_file=geoid{args.g}_{args.r}_tel_aligned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)



    print('\n\n###### alignment dut 1 #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_dut} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_tel_geo} -o detectors_file_updated={align_dut_geo_itr1} -o histogram_file=geoid{args.g}_{args.r}_dut_aligned_itr1.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n\n###### alignment dut 2 #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_dut} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_dut_geo_itr1} -o detectors_file_updated={align_dut_geo_itr2} -o histogram_file=geoid{args.g}_{args.r}_dut_aligned_itr2.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n\n###### alignment dut 3 #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_dut} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_dut_geo_itr2} -o detectors_file_updated={align_dut_geo_itr3} -o histogram_file=geoid{args.g}_{args.r}_dut_aligned_itr3.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n\n###### alignment dut final #########')
    corry_cmd = f'{corry_bin} -c {corry_config_align_dut} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_dut_geo_itr3} -o detectors_file_updated={align_dut_geo} -o histogram_file=geoid{args.g}_{args.r}_dut_aligned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)


else:
    pass