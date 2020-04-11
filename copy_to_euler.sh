printf "Copying files to location $1@euler.ethz.ch:wat_bal_python \n"
printf "Copying Data \n"
scp -r data $1@euler.ethz.ch:wat_bal_python
printf "Copying python scripts \n"
scp {run_opt,run_sim,utils,model}.py $1@euler.ethz.ch:wat_bal_python
printf "Copying parameter.h5 file \n"
scp parameters.h5 $1@euler.ethz.ch:wat_bal_python
printf "Copying Euler Scripts \n"
scp run.sh $1@euler.ethz.ch:wat_bal_python