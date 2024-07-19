#!/bin/bash

# Procedure: prealignment with telescope and DUT, telescope alignment (3 iterations), DUT alignment (2 iterations)
# before alignment: change initial geo (line 31)

RUN_NUMBER="$1"
GEOID="$2"

# Configuration of globally used paths

RAW_DIR="/home/bgnet/beam_data/raw_files"
ROOT_DIR="/home/bgnet/corry_config_desytb_2024"

echo "Starting Run $RUN_NUMBER"

FILE_TEL=`ls $RAW_DIR/telescope_run$RUN_NUMBER*`
FILE_MPX=`ls $RAW_DIR/mpx2_run$RUN_NUMBER*`


echo "Found TEL RAW file: $FILE_TEL"
echo "Found MPX2 RAW file: $FILE_MPX"


# Prealignment telescope

CORRY_CONFIG="$ROOT_DIR/prealign_tel_mpx2.conf"
ROOT_FILE="prealign_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

corry  -c $CORRY_CONFIG \
-o detectors_file="$ROOT_DIR/geo/init_geo/geo_id${GEOID}.geo" \
-o detectors_file_updated="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_prealigned.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR/output/alignment_root" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 


# Telescope alignment 1

CORRY_CONFIG="$ROOT_DIR/align_tel_mpx2.conf"
ROOT_FILE="align_tel1_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

corry  -c $CORRY_CONFIG \
-o detectors_file="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_prealigned.geo" \
-o detectors_file_updated="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_1.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR/output/alignment_root" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 


# Telescope alignment 2

CORRY_CONFIG="$ROOT_DIR/align_tel_mpx2.conf"
ROOT_FILE="align_tel2_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

corry  -c $CORRY_CONFIG \
-o detectors_file="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_1.geo"  \
-o detectors_file_updated="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_2.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR/output/alignment_root" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 


# Telescope alignment 3

CORRY_CONFIG="$ROOT_DIR/align_tel_mpx2.conf"
ROOT_FILE="align_tel3_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

corry  -c $CORRY_CONFIG \
-o detectors_file="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_2.geo" \
-o detectors_file_updated="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_3.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR/output/alignment_root" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 


# DUT alignment 1

CORRY_CONFIG="$ROOT_DIR/align_dut_mpx2.conf"
ROOT_FILE="align_dut1_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

corry  -c $CORRY_CONFIG \
-o detectors_file="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_tel_align_3.geo" \
-o detectors_file_updated="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_dut_align_1.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR/output/alignment_root" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\"


# DUT alignment 2

CORRY_CONFIG="$ROOT_DIR/align_dut_mpx2.conf"
ROOT_FILE="align_dut2_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"

corry  -c $CORRY_CONFIG \
-o detectors_file="$ROOT_DIR/geo/align_geo/${RUN_NUMBER}_detectors_dut_align_1.geo" \
-o detectors_file_updated="$ROOT_DIR/geo/full_aligned/${RUN_NUMBER}_full_aligned.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR/output/alignment_root" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" 
