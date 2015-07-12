#! /bin/bash

#for scale in `seq 0 10`; do
#	for file in `ls scale/pa*.ply`; do
#		base=$(basename $file)
#		output=${base%-nc.*}
#		./pymeshtoolkit.py -nc -cm Jet -o $output-nc.ply $file
#	done
#done

for scale in 1 2 3 4 5 6 7 8 9 10; do
		./pymeshtoolkit.py -glut "scale/pa-x$scale.ply"
		./pymeshtoolkit.py -glut "scale/pa-x$scale-nc.ply"
done
