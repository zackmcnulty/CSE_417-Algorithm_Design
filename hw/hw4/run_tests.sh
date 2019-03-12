#!/bin/bash

# useful for generating and running a bunch of test files.
# If passed arguments (same that make_random_test_files.py takes) then it generates test
# files AND runs. Otherwise, just runs test files in the "test_files/" folder in the current
# working directory
if ! test -z $1
then 
rm test_files/*
python3 make_random_test_files.py $1 $2 $3 $4 $5 $6
fi

for fn in $(ls test_files/);
do

echo "Running test for $fn"
python3 hw4_q3.py test_files/$fn


done
