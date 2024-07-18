#!/bin/bash

#Procedure: prealignment with telescope and DUT, telescope alignment (3 iterations), DUT alignment (2 iterations)
#before alignment: change initial geo (line 31)

RUN_NUMBER="$1"

#Configuration of globally used paths

RAW_DIR="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/data"
ROOT_DIR="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/output/alignment_root"
CORRY_CONFIG="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/prealign_tel_mpx2.conf"


echo "Starting Run $RUN_NUMBER"

FILE_TEL=`ls $RAW_DIR/telescope_run$RUN_NUMBER*`
FILE_MPX=`ls $RAW_DIR/mpx2_run$RUN_NUMBER*`


echo "Found TEL RAW file: $FILE_TEL"
echo "Found MPX2 RAW file: $FILE_MPX"


#Prealignment telescope

ROOT_FILE="prealign_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

/home/silicon/TJ-Monopix2/corryvreckan/bin/corry  -c $CORRY_CONFIG \
-o detectors_file="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/init_geo/geo_id3.txt" \
-o detectors_file_updated="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_prealigned.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 


#Align Tel 1

CORRY_CONFIG="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/align_tel_mpx2.conf"
ROOT_FILE="align_tel1_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

/home/silicon/TJ-Monopix2/corryvreckan/bin/corry  -c $CORRY_CONFIG \
-o detectors_file="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_prealigned.geo" \
-o detectors_file_updated="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_1.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 



#Align Tel 1

CORRY_CONFIG="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/align_tel_mpx2.conf"
ROOT_FILE="align_tel2_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

/home/silicon/TJ-Monopix2/corryvreckan/bin/corry  -c $CORRY_CONFIG \
-o detectors_file="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_1.geo" \
-o detectors_file_updated="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_2.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 



#Align Tel 3

CORRY_CONFIG="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/align_tel_mpx3.conf"
ROOT_FILE="align_tel3_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

/home/silicon/TJ-Monopix2/corryvreckan/bin/corry  -c $CORRY_CONFIG \
-o detectors_file="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_2.geo" \
-o detectors_file_updated="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_3.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 



#Telescope is now aligned, starting with DUT alignment


CORRY_CONFIG="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/align_dut_mpx2.conf"
ROOT_FILE="align_dut1_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

/home/silicon/TJ-Monopix2/corryvreckan/bin/corry  -c $CORRY_CONFIG \
-o detectors_file="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_3.geo" \
-o detectors_file_updated="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_dut_align_1.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\"


CORRY_CONFIG="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/align_dut_mpx2.conf"
ROOT_FILE="align_dut1_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

/home/silicon/TJ-Monopix2/corryvreckan/bin/corry  -c $CORRY_CONFIG \
-o detectors_file="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/align_geo/${RUN_NUMBER}_detectors_dut_align_1.geo" \
-o detectors_file_updated="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/full_aligned/${RUN_NUMBER}_full_aligned.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 