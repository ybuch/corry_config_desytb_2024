#!/bin/bash

RAW_DIR="<path_to_data>"

write_csv(){
    echo \"$1\", \"$2\", \"$3\", \"$4\" >> test.csv
}

write_csv RunNumber telescopeGeometry tel_data mpx_data

while IFS=, read -r RUN GEO_ID;
do 
    FILE_TEL=`ls $RAW_DIR/telescope_run$RUN*`
    FILE_MPX=`ls $RAW_DIR/mpx2_run$RUN*`
    write_csv $RUN ../geo/temp/dut_align_run_$RUN.geo $FILE_TEL $FILE_MPX

done < ../conf/W08R06_p.csv	#insert csv for output

sed 's/["]//g' test.csv > data_p.csv
rm test.csv
