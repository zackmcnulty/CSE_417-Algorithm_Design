for fn in $(ls test_files/);
do

echo "Running test for $fn"
python3 hw4_q3.py test_files/$fn


done
