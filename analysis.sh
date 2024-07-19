#!/bin/bash

RUN_NUMBER="$1"

RAW_DIR="/home/bgnet/beam_data/raw_files"
ROOT_DIR="/home/bgnet/corry_config_desytb_2024"


echo "Starting Run $RUN_NUMBER"

FILE_TEL=`ls $RAW_DIR/telescope_run$RUN_NUMBER*`
FILE_MPX=`ls $RAW_DIR/mpx2_run$RUN_NUMBER*`


echo "Found TEL RAW file: $FILE_TEL"
echo "Found MPX2 RAW file: $FILE_MPX"

CORRY_CONFIG="$ROOT_DIR/analysis.conf"
ROOT_FILE="analysis_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"


corry  -c $CORRY_CONFIG \
-o detectors_file="$ROOT_DIR/geo/full_aligned/${RUN_NUMBER}_full_aligned.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR/output" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" 


#-o detectors_file="/home/silicon/Desktop/Testfolder_DESY_07.24/data/geo_updated/${RUN_NUMBER}_dut3_aligned.geo" \
