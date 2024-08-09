#!/bin/bash
# Basic range in for loop
for run in {1441..1442}
    do
        touch mask_ref0_run$run.txt
        touch mask_ref1_run$run.txt
        touch mask_ref2_run$run.txt
        touch mask_ref3_run$run.txt
        touch mask_ref4_run$run.txt
        touch mask_ref5_run$run.txt
        touch mask_dut_run$run.txt
        # echo mask_ref0_$run.txt
    done
echo All done
