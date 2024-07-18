#!/bin/bash



RUN_NUMBER="$1"


RAW_DIR="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/data"
ROOT_DIR="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/output"
CORRY_CONFIG="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/analysis.conf"

echo "Starting Run $RUN_NUMBER"

FILE_TEL=`ls $RAW_DIR/telescope_run$RUN_NUMBER*`
FILE_MPX=`ls $RAW_DIR/mpx2_run$RUN_NUMBER*`


echo "Found TEL RAW file: $FILE_TEL"
echo "Found MPX2 RAW file: $FILE_MPX"


ROOT_FILE="analysis_run_$RUN_NUMBER.root"
echo "Output root file: $ROOT_FILE"


#rm -r -f ./output/MaskCreator/M*
#cp -r ./output/MaskCreator/finished_masksmasks_$RUN_NUMBER/M* ./output/MaskCreator/
#echo "Mask files of run $RUN_NUMBER set"


/home/silicon/TJ-Monopix2/corryvreckan/bin/corry  -c $CORRY_CONFIG \
-o detectors_file="/media/silicon/60080e46-ab47-4d7b-9668-26cd42445d81/corry_analysis/geo/full_aligned/geo_id3_full_aligned.geo" \
-o histogram_file="$ROOT_FILE" \
-o output_directory="$ROOT_DIR" \
-o EventLoaderEUDAQ2:Monopix2_0.file_name=\"$FILE_MPX\" \
-o EventLoaderEUDAQ2:MIMOSA26_0.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_1.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_2.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_3.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_4.file_name=\"$FILE_TEL\" \
-o EventLoaderEUDAQ2:MIMOSA26_5.file_name=\"$FILE_TEL\" 


#-o detectors_file="/home/silicon/Desktop/Testfolder_DESY_07.24/data/geo_updated/${RUN_NUMBER}_dut3_aligned.geo" \