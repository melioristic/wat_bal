module load new gcc/4.8.2 python/3.7.1
bsub -n 1 -W 4:00 -R "rusage[mem=1024]" python ./run_opt.py
