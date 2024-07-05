import argparse
import glob
import re
import os

#data_folder = '/home/testbeam1/data/data_producer_runs/desy'
data_folder = '/home/bgnet/corry_tutorial'
corry_bin = '~/vtx/corryvreckan/bin/corry'
corry_config_prealign_tel = 'prealign_tel_mpx2.conf'
corry_config_align_tel = 'align_tel_mpx2.conf'
corry_config_prealign_dut = 'prealign_dut_mpx2.conf'
corry_config_align_dut = 'align_dut_mpx2.conf'
geo_path = '/home/bgnet/corry_tutorial/'
output_dir = './corry_out/align_out'

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
prealign_tel_geo = geo_path + f'geoid{args.g}_tel_prealigned.geo'
align_tel_geo = geo_path + f'geoid{args.g}_tel_aligned.geo'
prealign_dut_geo = geo_path + f'geoid{args.g}_dut_prealigned.geo'
align_dut_geo = geo_path + f'geoid{args.g}_dut_aligned.geo'

if not args.o:

    print('\n\n##################################################### prealigning telescope ####################################')
    corry_cmd = f'{corry_bin} -c {corry_config_prealign_tel} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={rough_geo} -o detectors_file_updated={prealign_tel_geo} -o histogram_file=geoid{args.g}_tel_prealigned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n##################################################### aligning telescope ####################################')
    corry_cmd = f'{corry_bin} -c {corry_config_align_tel} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={prealign_tel_geo} -o detectors_file_updated={align_tel_geo} -o histogram_file=geoid{args.g}_tel_aligned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n##################################################### prealigning DUT ####################################')
    corry_cmd = f'{corry_bin} -c {corry_config_prealign_dut} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_tel_geo} -o detectors_file_updated={prealign_dut_geo} -o histogram_file=geoid{args.g}_dut_prealigned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)

    print('\n##################################################### aligning DUT ####################################')
    corry_cmd = f'{corry_bin} -c {corry_config_align_dut} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={prealign_dut_geo} -o detectors_file_updated={align_dut_geo} -o histogram_file=geoid{args.g}_dut_aligned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)
else:

    align_tel_geo = geo_path + f'geoid{args.o}_tel_aligned.geo'  # using old telescope alignment for new alignment of DUT only

    print('\n\n##################################################### prealigning DUT ####################################')
    corry_cmd = f'{corry_bin} -c {corry_config_prealign_dut} -o number_of_events={args.n} -o output_directory={output_dir} -o detectors_file={align_tel_geo} -o detectors_file_updated={prealign_dut_geo} -o histogram_file=geoid{args.g}_dut_prealigned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)


    align_tel_geo = geo_path + f'geoid{args.g}_tel_aligned.geo'
    print('\n##################################################### aligning DUT ####################################')
    corry_cmd = f'{corry_bin} -c {corry_config_align_dut} -o number_of_events={args.n} -o output_directory={output_dir}  -o detectors_file={prealign_dut_geo} -o detectors_file_updated={align_dut_geo} -o histogram_file=geoid{args.g}_dut_aligned.root -o EventLoaderEUDAQ2.file_name={current_tel_file} -o EventLoaderEUDAQ2:Monopix2_0.file_name={current_dut_file}'
    os.system(corry_cmd)
