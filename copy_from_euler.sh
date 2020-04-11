printf "Copying files from $1@euler.ethz.ch:wat_bal_python \n"
printf "Copying Parameter.h5 \n"
scp $1@euler.ethz.ch:wat_bal_python/parameters.h5 .
printf "Copying plots \n"
scp -r $1@euler.ethz.ch:wat_bal_python/plots .