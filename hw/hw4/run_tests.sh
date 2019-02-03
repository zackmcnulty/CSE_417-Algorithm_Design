if ! test -z $1
then 
rm test_files/*
python3 make_random_test_files.py $1 $2 $3 $4
fi

for fn in $(ls test_files/);
do

echo "Running test for $fn"
python3 hw4_q3.py test_files/$fn


done
