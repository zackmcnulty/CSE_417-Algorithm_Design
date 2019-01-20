#!/bin/bash
for fn in $(ls biconnectivity-tests/tests/) ; do
	python3 hw2.py biconnectivity-tests/tests/$fn
done
