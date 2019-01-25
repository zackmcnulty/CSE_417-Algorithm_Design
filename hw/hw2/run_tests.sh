#!/bin/bash
#for fn in $(ls biconnectivity-tests/tests/) ; do
#	printf  " %s" "$fn"
#	python3 hw2.py biconnectivity-tests/tests/$fn
#done

for fn in $(ls bigs/n2048*) ; do
	printf  " %s" "$fn"
	python3 hw2.py $fn
done
