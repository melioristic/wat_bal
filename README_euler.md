### Running Scripts on Euler

- Step I : Open Terminal/PowerShell
- Step II : Run the command `ssh username@euler.ethz.ch`
- Step III : Enter the password when prompted
- Step IV : In the euler terminal enter the command `mkdir wat_bal_python`
- Step V : Then exit the terminal with `exit` command
- Step VI : Navigate to the directory of your project folder
- Step VI : run the command `./copy_to_euler.sh username`
- Step (Optional) : If you see the permission denied message then run the command `chmod +x copy_to_euler.sh`
- Step VII : Enter the password, you will be asked password 4 times
- Step VIII : In a new terminal (or the same terminal) login to euler cluster with the command `ssh username@euler.ethz.ch`
- Step IX : Change directory to wat_bal_python with `cd wat_bal_python`
- Step X : Run the job at cluster using the command `./run.sh`
- Step XI : Once the job is finished, copy the parameters and plots to your computer by running the script `copy_from_euler.sh username`. If you dont have any plots folder then you can comment the line to copy plots in the copy_from_euler.sh file

### Other Info
- You can check the running jobs with the command `bjobs`
- You can kill a job with the command `bkill job_id`
- You can modify the run.sh script to run run_opt.py or run_sim.py
- You can run multiple jobs at once but just take care of dependencies. 
    - Like run_sim.py needs to access parameters.h5 file and two scripts cannot open the same h5py file simultaneously
    - If you plan to run multiple optimization algorithms at once make sure all of them saves the parameters in different h5py file.
