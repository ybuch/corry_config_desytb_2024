#!/bin/bash

for i in $(seq 0 1 500); do
    echo "c $i" >> mask.txt
done
